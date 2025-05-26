from .logger import get_logger

logger = get_logger(__name__)


def handle_error(exception):
    logger.error(f"Exception occurred: {str(exception)}")
    raise exception
