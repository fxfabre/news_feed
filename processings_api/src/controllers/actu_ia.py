import html
import logging

from bs4 import BeautifulSoup
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from src.models.actu_ia_article import ActuIaArticle
from src.models.email_content import EmailContent
from src.models.web_urls import WebUrls, WebUrl

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/extract_links", response_class=ORJSONResponse)
def extract_links_from_actu_ia(email: EmailContent) -> ORJSONResponse:
    text = html.unescape(email.text_as_html)
    text = text.replace("<br/>", " ")

    links = []
    for txt_bloc in text.split("Lire l'article")[1:]:
        soup = BeautifulSoup(txt_bloc)
        link = soup.find("a").text
        links.append(link)
    return ORJSONResponse(links)


@router.post("/summarize_list", response_class=ORJSONResponse)
def summarize(actu_ia_urls: WebUrls) -> ORJSONResponse:
    data_out = []
    for url in actu_ia_urls.urls:
        article = ActuIaArticle(url)
        data_out.append({"title": article.title, "en_bref": article.en_bref})

    return ORJSONResponse({"texts_summary": data_out})


@router.post("/summarize_str", response_class=ORJSONResponse)
def summarize(actu_ia_url: WebUrl) -> ORJSONResponse:
    article = ActuIaArticle(actu_ia_url.url)
    return ORJSONResponse({"title": article.title, "en_bref": article.en_bref})
