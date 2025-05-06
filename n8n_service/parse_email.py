import json
import html
import requests
from unidecode import unidecode
from pprint import pprint
from bs4 import BeautifulSoup
import random
import time


def parse_actu_ia(html_content):
    text = html.unescape(html_content)
    text = text.replace("<br/>", " ")

    sleep_time = 0
    for txt_bloc in text.split("Lire l'article")[1:]:
        soup = BeautifulSoup(txt_bloc)
        link = soup.find("a").text

        time.sleep(sleep_time)
        response = requests.get(link)
        article = BeautifulSoup(response.text)
        content = article.find("div", {"class": "articleBody"}).text.strip()
        yield unidecode(content)

        sleep_time = random.uniform(3, 6)


def main(raw_input):
    processor = {
        "contact@actuia.com": parse_actu_ia,
    }
    
    for item in raw_input.all():
        html_content = item.json.textAsHtml
        sender = item.json["from"]["value"][0]["address"]

        func = processor[sender]
        yield from func(html_content)
    

main(_input)
