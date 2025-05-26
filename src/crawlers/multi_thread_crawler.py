import threading
from src.crawlers.youtube_crawler import crawl_youtube
from src.crawlers.vimeo_crawler import crawl_vimeo
from src.crawlers.api_crawler import crawl_api
from src.crawlers.web_crawler import crawl_web
from src.crawlers.keyword_generator import generate_keywords
from src.utils.logger import get_logger

logger = get_logger(__name__)


def crawl_multi_sources(sources, max_frames):
    keywords = generate_keywords()
    threads = []
    results = []

    def worker(source, keywords, max_frames):
        if source == "youtube":
            frames = crawl_youtube(keywords, max_frames)
        elif source == "vimeo":
            frames = crawl_vimeo(keywords, max_frames)
        elif source == "api":
            frames = crawl_api(keywords, max_frames)
        elif source == "web":
            frames = crawl_web(keywords, max_frames)
        else:
            frames = []
        results.extend(frames)

    for source in sources:
        thread = threading.Thread(target=worker, args=(source, keywords, max_frames))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    logger.info(f"Total frames collected from {sources}: {len(results)}")
    return results
