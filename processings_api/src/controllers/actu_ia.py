import html
import logging
from typing import Iterable

from bs4 import BeautifulSoup
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.models.email_content import EmailContent

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/extract_links", response_class=JSONResponse)
def extract_links_from_actu_ia(email_contents: list[EmailContent]) -> Iterable[str]:
    for email_content in email_contents:
        text = html.unescape(email_content.html_content)
        text = text.replace("<br/>", " ")

        for txt_bloc in text.split("Lire l'article")[1:]:
            soup = BeautifulSoup(txt_bloc)
            link = soup.find("a").text
            yield link
