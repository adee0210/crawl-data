import os
import cv2
import yt_dlp
from src.utils.logger import get_logger
from src.utils.error_handler import handle_error
import uuid

logger = get_logger(__name__)


def crawl_youtube(keywords, max_frames, min_duration=30, max_duration=900):
    try:
        frame_paths = []
        frame_count = 0
        ydl_opts = {
            "format": "bestvideo[height<=1080]",
            "outtmpl": "/tmp/youtube_video_%(id)s.%(ext)s",
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for keyword in keywords:
                if frame_count >= max_frames:
                    break
                search_url = f"ytsearch10:{keyword} football"
                result = ydl.extract_info(search_url, download=True)
                entries = result.get("entries", [])

                for entry in entries:
                    if frame_count >= max_frames:
                        break
                    duration = entry.get("duration", 0)
                    if min_duration <= duration <= max_duration:
                        video_id = entry.get("id", str(uuid.uuid4()))
                        ext = entry.get("ext", "mp4")
                        video_path = f"/tmp/youtube_video_{video_id}.{ext}"

                        if (
                            not os.path.exists(video_path)
                            or os.path.getsize(video_path) == 0
                        ):
                            logger.error(f"Video file not found or empty: {video_path}")
                            continue

                        new_frames = extract_frames(video_path, frame_count, max_frames)
                        frame_paths.extend(new_frames)
                        frame_count = len(frame_paths)

                        try:
                            os.remove(video_path)
                        except Exception as e:
                            logger.warning(
                                f"Could not delete video file {video_path}: {e}"
                            )

                        logger.info(
                            f"Extracted frames from YouTube video: {entry['webpage_url']}"
                        )

        return frame_paths
    except Exception as e:
        handle_error(e)
        logger.error(f"Error in crawl_youtube: {str(e)}")
        return []


def extract_frames(video_path, current_count, max_frames):
    frames = []
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25

    frame_interval = int(fps)

    while cap.isOpened() and current_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        if frame_count % frame_interval == 0:
            frame_path = f"/tmp/frame_{current_count}.jpg"
            cv2.imwrite(frame_path, frame)
            frames.append(frame_path)
            current_count += 1
    cap.release()
    return frames
