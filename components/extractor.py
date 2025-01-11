from bs4 import BeautifulSoup

class HtmlLinkExtractor:
    def extract_links(self, html: str, base_url: str) -> list[str]:
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/'):
                links.append(base_url + href)
            elif href.startswith(base_url):
                links.append(href)
        return links
