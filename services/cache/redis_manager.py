from typing import Optional, override
from redis.asyncio import Redis
from domain.cache.cache_manager_interface import CacheManagerInterface
from domain.settings import get_settings


class RedisManager(CacheManagerInterface):

    def __init__(self):
        settings = get_settings()
        redis_url = f"redis://default:{settings.redis_password}@{settings.redis_host}:{settings.redis_port}"
        self.redis_conn: Redis = Redis.from_url(redis_url)

    @override
    async def create_new_job_status(self, key: str) -> bool:
        """
        Initialize a job status in Redis with 'running' value.
        """
        created = await self.redis_conn.set(f"job:{key}", "running", nx=True)
        return bool(created)

    @override
    async def set_job_status(self, key: str, status: str) -> None:
        """
        Update the status of a job in Redis.
        """
        await self.redis_conn.set(f"job:{key}", status)

    @override
    async def get_job_status(self, key: str) -> Optional[str]:
        """
        Retrieve the current status of a job. Returns None if not found.
        """
        status = await self.redis_conn.get(f"job:{key}")
        if status is None:
            return None
        return status.decode("utf-8")

    async def close(self) -> None:
        """
        Close Redis connection.
        """
        await self.redis_conn.close()
