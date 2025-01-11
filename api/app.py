from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from components.fetcher import HttpFetcher
from components.extractor import HtmlLinkExtractor
from components.matcher import RegexUrlMatcher
from components.result_handler import JsonResultHandler
from crawler.crawler import WebCrawler
import asyncio
import logging

app = FastAPI()

# Initialize shared objects
fetcher = HttpFetcher()
extractor = HtmlLinkExtractor()
matcher = RegexUrlMatcher()
result_handler = JsonResultHandler()

# Dictionary to store crawl statuses and results
crawl_status = {}
crawlers = {}

# Setup logging
logger = logging.getLogger("web_crawler")
logging.basicConfig(level=logging.INFO)

class CrawlRequest(BaseModel):
    domains: list[str]
    max_depth: int = 3
    global_timeout: int = 60


@app.post("/start-crawl")
async def start_crawl(request: CrawlRequest, background_tasks: BackgroundTasks):
    """
    Start a crawl for the specified domains.
    """
    crawl_id = str(len(crawl_status) + 1)
    crawl_status[crawl_id] = {"status": "running", "results": None}

    def run_crawler():
        nonlocal crawl_id
        crawler = WebCrawler(
            request.domains,
            fetcher,
            extractor,
            matcher,
            result_handler,
            max_depth=request.max_depth,
            global_timeout=request.global_timeout,
        )
        crawlers[crawl_id] = crawler
        try:
            asyncio.run(crawler.run())
            crawler.save_results()
            crawl_status[crawl_id]["status"] = "completed"
            crawl_status[crawl_id]["results"] = crawler.results
        except Exception as e:
            logger.error(f"Crawl failed: {e}")
            crawl_status[crawl_id]["status"] = "failed"

    background_tasks.add_task(run_crawler)
    return {"crawl_id": crawl_id, "status": "started"}


@app.get("/crawl-status/{crawl_id}")
async def get_crawl_status(crawl_id: str):
    """
    Get the status of a crawl.
    """
    if crawl_id not in crawl_status:
        return {"error": "Crawl ID not found"}
    return crawl_status[crawl_id]


@app.get("/results/{crawl_id}")
async def get_crawl_results(crawl_id: str):
    """
    Get the results of a completed crawl.
    """
    if crawl_id not in crawl_status:
        return {"error": "Crawl ID not found"}
    if crawl_status[crawl_id]["status"] != "completed":
        return {"error": "Crawl is not yet completed or has failed"}
    return crawl_status[crawl_id]["results"]
