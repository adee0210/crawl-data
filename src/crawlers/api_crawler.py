import os
import requests
import cv2
from src.utils.logger import get_logger
from src.utils.error_handler import handle_error

logger = get_logger(__name__)


def crawl_api(keywords, max_frames, min_duration=30, max_duration=900):
    try:
        frame_paths = []
        frame_count = 0
        api_key = os.getenv("SPORT_API_KEY")
        api_url = "https://api.sportplatform.com/videos"

        for keyword in keywords:
            if frame_count >= max_frames:
                break
            response = requests.get(
                f"{api_url}?query={keyword}&api_key={api_key}&limit=10"
            )
            videos = response.json().get("videos", [])

            for video in videos:
                if frame_count >= max_frames:
                    break
                duration = video.get("duration", 0)
                if min_duration <= duration <= max_duration:
                    video_url = video.get("url")
                    if video_url:
                        video_path = download_video(video_url)
                        frame_paths.extend(
                            extract_frames(video_path, frame_count, max_frames)
                        )
                        frame_count = len(frame_paths)
                        os.remove(video_path)
                        logger.info(f"Extracted frames from API video: {video_url}")

        return frame_paths
    except Exception as e:
        handle_error(e)
        logger.error(f"Error in crawl_api: {str(e)}")
        return []


def download_video(url):
    response = requests.get(url, stream=True)
    video_path = "/tmp/api_video.mp4"
    with open(video_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return video_path


def extract_frames(video_path, current_count, max_frames):
    frames = []
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
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
