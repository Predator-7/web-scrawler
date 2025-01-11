import aiohttp
import logging
import asyncio

class HttpFetcher:
    def __init__(self, max_concurrent_requests=10):
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def fetch(self, url):
        async with self.semaphore:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            return await response.text()
            except Exception as e:
                print(f"Error fetching {url}: {e}")
        return None
