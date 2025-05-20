import io
import logging
import os.path
from collections.abc import Generator

import nltk
import numpy as np
from bark import SAMPLE_RATE, semantic_to_waveform
from bark.generation import generate_text_semantic
from fastapi import APIRouter
from fastapi.responses import Response
from scipy.io.wavfile import write as write_wav

from tts_api.models.tts_request import TtsRequest

logger = logging.getLogger(__name__)
router = APIRouter()
GEN_TEMP = 0.6


@router.post("/binary", response_class=Response)
async def generate_speech(body: TtsRequest) -> Response:
    pieces = list(text_to_audio(body.text, body.language))

    with io.BytesIO() as audio_file:
        write_wav(audio_file, SAMPLE_RATE, np.concatenate(pieces))
        audio_file.seek(0)
        content = audio_file.read()

    return Response(content=content, media_type="audio/wav")


def text_to_audio(text: str, language: str) -> Generator[np.array, None, None]:
    voice_preset = f"v2/{language}_speaker_2"
    cache_file = f"/tts_cache/{voice_preset}.json"
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)

    updated_cache = False
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "rb") as f:
                cache = dict(np.load(f))
        except Exception:
            logger.exception("Unable to load cache")
            cache = {}
    else:
        cache = {}

    silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence
    for sentence in nltk.sent_tokenize(text):
        if sentence.lower() in cache:
            logger.debug("Cache   to audio : %s", sentence)
            audio_array = cache[sentence.lower()]
        else:
            logger.debug("Convert to audio : %s", sentence)
            audio_array = sentense_to_audio(sentence, voice_preset)
            cache[sentence.lower()] = audio_array
            updated_cache = True

        yield np.concatenate([audio_array, silence])

    if updated_cache:
        with open(cache_file, "wb+") as f:
            np.savez_compressed(f, **cache)


def sentense_to_audio(sentence: str, voice_preset: str) -> np.array:
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
    return audio_array
