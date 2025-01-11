import re

class RegexUrlMatcher:
    def __init__(self, patterns: list[str] = None):
        self.patterns = patterns or [r'/product/', r'/item/', r'/p/', r'/shop/']

    def is_product_url(self, url: str) -> bool:
        return any(re.search(pattern, url) for pattern in self.patterns)
