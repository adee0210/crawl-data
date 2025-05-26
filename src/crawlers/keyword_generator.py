import yaml
from src.utils.logger import get_logger

logger = get_logger(__name__)


def generate_keywords():
    try:
        with open("/home/duc/video_pipeline_project/config.yaml", "r") as f:
            config = yaml.safe_load(f)

        keywords = config.get(
            "keywords", ["football", "soccer", "match highlights", "goal compilation"]
        )
        logger.info(f"Generated keywords: {keywords}")
        return keywords
    except Exception as e:
        logger.error(f"Error generating keywords: {str(e)}")
        return ["football", "soccer"]
