import json
import logging
import os.path

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
    voice_preset = f"v2/{language}_speaker_2"
    cache_file = f"/tts_cache/{voice_preset}.json"
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)

    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cache = json.load(f)
    else:
        cache = {}

    silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence
    for sentence in nltk.sent_tokenize(text):
        logger.debug("Convert to audio : %s", sentence)

        if sentence in cache:
            audio_array = cache[sentence]
        else:
            audio_array = sentense_to_audio(sentence, voice_preset)
            cache[sentence] = audio_array

        yield np.concatenate([audio_array, silence])

    with open(cache_file, "w+") as f:
        json.dump(cache, f)


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
