import logging

import nltk
import numpy as np
from bark import SAMPLE_RATE, semantic_to_waveform
from bark.generation import generate_text_semantic
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from tts_api.models.tts_request import TtsRequest
from tts_api.models.wavefile_content import AudioSegment

logger = logging.getLogger(__name__)
router = APIRouter()
MODEL_NAME = "suno/bark-small"
GEN_TEMP = 0.6


@router.post("/", response_model=AudioSegment, response_class=ORJSONResponse)
async def generate_speech(body: TtsRequest) -> AudioSegment:
    pieces = list(text_to_audio(body.text, body.language))

    return AudioSegment(
        rate=SAMPLE_RATE,
        data=np.concatenate(pieces).tolist(),
        content_type="audio/wav",
    )


def text_to_audio(text: str, language: str) -> AudioSegment:
    silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence
    voice_preset = f"v2/{language}_speaker_2"

    for sentence in nltk.sent_tokenize(text):
        logger.debug("Convert to audio : %s", sentence)

        semantic_tokens = generate_text_semantic(
            sentence,
            history_prompt=voice_preset,
            temp=GEN_TEMP,
            min_eos_p=0.05,  # this controls how likely the generation is to end
        )

        audio_array = semantic_to_waveform(
            semantic_tokens,
            history_prompt=voice_preset,
        )
        yield np.concatenate([audio_array, silence])
