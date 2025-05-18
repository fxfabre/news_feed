import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AudioSegment(BaseModel):
    rate: int
    data: list[float]
    content_type: str = "audio/wav"
