import os
import cv2
import zipfile
from datetime import datetime
from ultralytics import YOLO
from src.storage.s3_storage import upload_to_s3
from src.utils.logger import get_logger
from src.utils.error_handler import handle_error

logger = get_logger(__name__)


def process_frames(source):
    try:
        frame_dir = "/tmp"
        model = YOLO("yolov8s.pt")

        frames = [f for f in os.listdir(frame_dir) if f.endswith(".jpg")]
        labels = []

        for frame_path in frames:
            full_path = os.path.join(frame_dir, frame_path)
            img = cv2.imread(full_path)
            results = model(img)

            for result in results:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = f"{model.names[cls]} {conf:.2f}"
                    labels.append(f"{frame_path}: {label}")

            # Lưu ảnh nén
            compressed_path = os.path.join(frame_dir, f"{frame_path}.compressed.jpg")
            cv2.imwrite(compressed_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            os.remove(full_path)

        # Tạo file nhãn
        label_file = os.path.join(frame_dir, "labels.txt")
        with open(label_file, "w") as f:
            f.write("\n".join(labels))

        # Nén tất cả ảnh đã nén + file nhãn vào zip
        zip_name = f"{source}_{datetime.now().strftime('%Y%m%d')}.zip"
        zip_path = os.path.join("/tmp", zip_name)
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for frame in os.listdir(frame_dir):
                if frame.endswith(".compressed.jpg"):
                    zipf.write(os.path.join(frame_dir, frame), frame)
            zipf.write(label_file, "labels.txt")

        # Upload lên S3
        upload_to_s3(zip_path, os.getenv("S3_BUCKET"))

        # Xoá file tạm
        os.remove(zip_path)
        os.remove(label_file)
        for frame in os.listdir(frame_dir):
            if frame.endswith(".compressed.jpg"):
                os.remove(os.path.join(frame_dir, frame))

        logger.info(f"Processed and uploaded frames for {source}")

    except Exception as e:
        handle_error(e)
        logger.error(f"Error in process_frames: {str(e)}")
