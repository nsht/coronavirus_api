import asyncio
from aiocache import Cache
import requests
from app.secrets import *


def get_news(country_name="in"):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    cache = Cache(
        Cache.REDIS,
        endpoint="redis",
        port=6379,
        namespace="corona_api",
        timeout=60 * 30,
    )
    cached_data = loop.run_until_complete(cache.get(f"news_{country_name}"))
    if cached_data:
        return cached_data
    url = f"http://newsapi.org/v2/top-headlines?q=coronavirus\
        &sortBy=popularity&country={country_name}&apiKey={NEWS_API_KEY}"
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        loop.run_until_complete(cache.set(f"news_{country_name}", response))
        return data
