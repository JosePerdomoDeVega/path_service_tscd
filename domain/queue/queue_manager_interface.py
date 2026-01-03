from abc import ABC, abstractmethod
from domain.models.job import Job
from typing import List


class QueueManagerInterface(ABC):

    @abstractmethod
    def get_queued_jobs(self) -> List[Job]:
        """
        Get messages from queue.
        """
        pass

    @abstractmethod
    def delete_message(self, job: Job) -> None:
        """
        Get messages from queue.
        """
        pass
