from pydantic import BaseModel


class WebUrls(BaseModel):
    urls: list[str]

class WebUrl(BaseModel):
    url: str
