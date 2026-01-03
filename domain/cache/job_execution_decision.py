from domain.cache.cache_manager_interface import CacheManagerInterface
from domain.models.job import Job


async def i_can_execute_this_job(job: Job, cache_manager: CacheManagerInterface) -> bool:
    answer = await cache_manager.create_new_job_status(job.job_id)
    return answer
