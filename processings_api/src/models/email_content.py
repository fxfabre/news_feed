from pydantic import BaseModel


class EmailContent(BaseModel):
    html_content: str
