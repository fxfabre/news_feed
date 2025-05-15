from pydantic import BaseModel


class EmailContent(BaseModel):
    text_as_html: str
