from abc import ABC, abstractmethod


class CacheManagerInterface(ABC):

    @abstractmethod
    async def create_new_job_status(self, key) -> bool:
        """
        Create atomically a job in cache.
        :returns: True if the job was created, False otherwise.
        """
        pass


    @abstractmethod
    async def set_job_status(self, key, status) -> None:
        """
        Set atomically a job status.
        """
        pass

    @abstractmethod
    async def get_job_status(self, key) -> str:
        """
        Get atomically a job status.
        """
        pass
