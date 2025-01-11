from utils.logger import setup_logging
from components.fetcher import HttpFetcher
from components.extractor import HtmlLinkExtractor
from components.matcher import RegexUrlMatcher
from components.result_handler import JsonResultHandler
from crawler.crawler import WebCrawler
from config import DOMAINS

import asyncio

if __name__ == "__main__":
    logger = setup_logging()

 
    fetcher = HttpFetcher()
    extractor = HtmlLinkExtractor()
    matcher = RegexUrlMatcher()
    result_handler = JsonResultHandler()

    crawler = WebCrawler(DOMAINS, fetcher, extractor, matcher, result_handler)

    try:
        logger.info("Starting crawler...")
        asyncio.run(crawler.run())
        logger.info("Crawler finished successfully. Saving results...")
        crawler.save_results()
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
    finally:
        logger.info("Crawler execution completed.")
