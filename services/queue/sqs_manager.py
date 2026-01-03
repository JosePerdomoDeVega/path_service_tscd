from typing import override, List
import boto3
import json
from domain.models.job import Job
from domain.queue.queue_manager_interface import QueueManagerInterface
from domain.settings import get_settings
from services.logger.logger import get_logger
from services.queue.job_creation import get_job_from_sqs_message

logger = get_logger()


def get_job_id(message):
    return str(json.loads(message[0].get('body')).get('job_id'))


class SQSQueueManager(QueueManagerInterface):
    """
    AWS SQS implementation of QueueManagerInterface.
    """

    def __init__(self):
        settings = get_settings()
        self.queue_url = settings.sqs_queue_url
        self.sqs_client = boto3.client("sqs", region_name=settings.aws_region)

    @override
    def get_queued_jobs(self, max_messages: int = 10) -> List[Job]:
        """
        Receive messages from the queue.
        By default, retrieves up to 10 messages (SQS max batch size).
        Returns a list of dicts with 'body' and 'receipt_handle'.
        """
        try:
            response = self.sqs_client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=5
            )

            messages = response.get("Messages", [])
            result = []
            logger.info(f"Received {len(messages)} messages from queue")
            for msg in messages:
                result.append(get_job_from_sqs_message(msg))
            return result
        except Exception as e:
            logger.error("Failed to receive messages", error=str(e))
            return []

    @override
    def delete_message(self, job: Job) -> None:
        """
        Delete a message from the queue after processing it.
        """
        try:
            self.sqs_client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=job.receipt_handle,
            )
            logger.info("Message deleted", receipt_handle=job.receipt_handle)
        except Exception as e:
            logger.error("Failed to delete message", error=str(e))
            raise
