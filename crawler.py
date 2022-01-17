import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import elara
import re

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, visited_db ,urls=[], path = 'https://arxiv.org'):
        self.visited_urls = visited_db
        self.urls_to_visit = urls
        self.exp_paper = re.compile('.*/abs/.*')
        self.exp_index = re.compile('.*list/cs.*')

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            # result = False
            if type(path) == str:
                pat_1 = self.exp_index.match(path)
                pat_2 = self.exp_paper.match(path)
                if pat_1 or pat_2:
                    if path and path.startswith('/'):
                        path = urljoin(url, path)
                    yield path

    # TODO: extract fields into json.
    def extract_info(self,html):
        print(html)
        # soup = BeautifulSoup(html, 'html.parser')


    def add_url_to_visit(self, url):
        # pat_paper = self.exp_paper.match(url)
        if not self.visited_urls.get(url) and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)
        if self.exp_paper.match(url):
            self.extract_info(html)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            pat_paper = self.exp_paper.match(url)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                if pat_paper:
                    self.visited_urls[url] = 1

if __name__ == '__main__':
    # TODO Change elara to tinyDB. I think elara is great to try, but tinyDB would be perfect for our use.
    visited_db = elara.exe('visited.db',True)
    Crawler(urls=['https://arxiv.org/archive/cs'], visited_db=visited_db).run()
    # Crawler(urls=['https://arxiv.org/abs/1703.06868'], visited_db=visited_db).run()