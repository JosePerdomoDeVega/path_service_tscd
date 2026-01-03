from services.queue.sqs_manager import SQSQueueManager
from domain.settings import get_settings
from domain.queue.queue_manager_interface import QueueManagerInterface
from services.logger.logger import get_logger

settings = get_settings()
logger = get_logger()


def get_queue_manager() -> QueueManagerInterface:
    queue_manager = None
    if settings.queue_implementation == "AWS_SQS":
        queue_manager = SQSQueueManager()
        logger.info(f"Using {settings.queue_implementation} as queue manager")
    return queue_manager
