from services.cache.redis_manager import RedisManager
from domain.settings import get_settings
from domain.cache.cache_manager_interface import CacheManagerInterface
from services.logger.logger import get_logger

settings = get_settings()
logger = get_logger()


def get_cache_manager() -> CacheManagerInterface:
    cache_manager = None
    if settings.cache_implementation == "REDIS":
        cache_manager = RedisManager()
        logger.info(f"Using {settings.cache_implementation} as cache manager")
    return cache_manager
