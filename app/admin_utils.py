import asyncio
from aiocache import Cache


def purge_cache(cache_key="all_stats"):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    cache = Cache(
        Cache.REDIS,
        endpoint="redis",
        port=6379,
        namespace="corona_api",
        timeout=60 * 30,
    )
    loop.run_until_complete(cache.delete(cache_key))
    print(f"Purged {cache_key}")
