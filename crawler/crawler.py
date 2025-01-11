import asyncio
import logging

class WebCrawler:
    def __init__(self, domains, fetcher, extractor, matcher, result_handler, max_depth=3, global_timeout=60):
        self.domains = domains
        self.fetcher = fetcher
        self.extractor = extractor
        self.matcher = matcher
        self.result_handler = result_handler
        self.max_depth = max_depth
        self.global_timeout = global_timeout
        self.visited = set()
        self.queue = asyncio.Queue()
        self.results = {}

    async def crawl(self, domain: str):
        logging.info(f"Starting crawl for domain: {domain}")
        self.results[domain] = []
        await self.queue.put((domain, 0))

        while not self.queue.empty():
            url, depth = await self.queue.get()
            if depth > self.max_depth or url in self.visited:
                continue

            self.visited.add(url)
            html = await self.fetcher.fetch(url)
            if html:
                links = self.extractor.extract_links(html, domain)
                for link in links:
                    if link not in self.visited:
                        self.queue.put_nowait((link, depth + 1))
                        if self.matcher.is_product_url(link):
                            self.results[domain].append(link)
                            logging.info(f"Product URL discovered: {link}")

    async def run(self):
        try:
            logging.info("Starting crawler.")
            await asyncio.wait_for(
                asyncio.gather(*(self.crawl(domain) for domain in self.domains)),
                timeout=self.global_timeout,
            )
        except asyncio.TimeoutError:
            logging.error("Global timeout reached. Stopping crawler.")

    def save_results(self):
        self.result_handler.save_results(self.results)
