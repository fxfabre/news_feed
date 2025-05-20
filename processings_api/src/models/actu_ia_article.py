import datetime as dt
import json
import logging
import random
import threading
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
lock = threading.Lock()


class ActuIaArticle:
    def __init__(self, url: str):
        self.url = url
        self._content = None

    @property
    def content(self) -> str:
        if self._content:
            return self._content

        with open("/data/cache_articles/index_actu_ia.json", "r") as f:
            index = json.load(f)

        if self.url in index:
            logger.info("Get url content from cache : %s", self.url)
            content_file_path = index[self.url]
            content = Path(content_file_path).read_text()
        else:
            logger.info("Query url %s", self.url)
            content = requests.get(self.url).text
            time.sleep(random.random() * 3 + 1)

            file_path = "/data/cache_articles/" + dt.datetime.now().isoformat(sep="_") + ".html"
            with open(file_path, "w+") as f:
                f.write(content)

            with lock, open("/data/cache_articles/index_actu_ia.json", "w+") as f:
                index = json.load(f)
                if self.url not in index:
                    f.seek(0)
                    f.write(json.dumps(index | {self.url: file_path}, indent=4))

        self._content = content
        return self._content

    @property
    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.content)

    @property
    def title(self) -> str:
        soup = self.soup
        return (
            soup.find("h1", attrs={"itemprop": "headline"}) or soup.find("h1")
        ).text.strip()

    @property
    def en_bref(self) -> str:
        return self.soup.find("div", attrs={"itemprop": "articleBody"}).text.strip()

    @property
    def text_content(self) -> str:
        return self.soup.find_all("div", attrs={"itemprop": "articleBody"})[1].text.strip()
