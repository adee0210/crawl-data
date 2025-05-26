import os
import requests
from bs4 import BeautifulSoup
import cv2
from src.utils.logger import get_logger
from src.utils.error_handler import handle_error

logger = get_logger(__name__)


def crawl_web(keywords, max_frames, min_duration=30, max_duration=900):
    try:
        frame_paths = []
        frame_count = 0
        base_urls = ["https://footballhighlights.com", "https://soccerclips.net"]

        for keyword in keywords:
            if frame_count >= max_frames:
                break
            for base_url in base_urls:
                if frame_count >= max_frames:
                    break
                search_url = f"{base_url}/search?q={keyword}"
                response = requests.get(search_url)
                soup = BeautifulSoup(response.content, "html.parser")
                video_links = [
                    a["href"]
                    for a in soup.find_all("a", href=True)
                    if "video" in a["href"]
                ]

                for video_url in video_links[:5]:
                    if frame_count >= max_frames:
                        break
                    video_path = download_video(video_url)
                    frame_paths.extend(
                        extract_frames(video_path, frame_count, max_frames)
                    )
                    frame_count = len(frame_paths)
                    os.remove(video_path)
                    logger.info(f"Extracted frames from web video: {video_url}")

        return frame_paths
    except Exception as e:
        handle_error(e)
        logger.error(f"Error in crawl_web: {str(e)}")
        return []


def download_video(url):
    response = requests.get(url, stream=True)
    video_path = "/tmp/web_video.mp4"
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
