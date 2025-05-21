"""
Manage text to speech

You can either :
- Ask for the computation of a text.
  This will generate the audio from the text in a background task.
  And save it in an internal cache
  Endpoint: /api/v1/tts/submit
  return: Nothing (success response, code 202
- Ask for the generated audio
  It will only use the cache to generate an audio for the input text
  Endpoint: /api/v1/tts/wav
  return: a wav file (binary data)
"""

import io
import logging
import os.path
from collections.abc import Generator

import nltk
import numpy as np
from bark import SAMPLE_RATE, semantic_to_waveform
from bark.generation import generate_text_semantic
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse, Response
from scipy.io.wavfile import write as write_wav

from tts_api.models.tts_request import TtsRequest

logger = logging.getLogger(__name__)
router = APIRouter()
GEN_TEMP = 0.6


@router.post("/wav", response_class=Response)
async def generate_wav_from_cache(body: TtsRequest) -> Response:
    pieces = list(text_to_audio(body.text, body.language))

    with io.BytesIO() as audio_file:
        write_wav(audio_file, SAMPLE_RATE, np.concatenate(pieces))
        audio_file.seek(0)
        content = audio_file.read()

    return Response(content=content, media_type="audio/wav")


@router.post("/submit", response_class=Response)
async def submit_generate_audio(body: TtsRequest, background_tasks: BackgroundTasks) -> Response:
    background_tasks.add_task(text_to_audio, body.text, body.language)
    return JSONResponse({"status": "success"}, status_code=202)


def text_to_audio(text: str, language: str) -> Generator[np.array, None, None]:
    voice_preset = f"v2/{language}_speaker_2"
    cache_file = f"/shared/tts_cache/{voice_preset}.json"
    silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence

    cache = {}
    try:
        with open(cache_file, "rb") as f:
            cache = dict(np.load(f))
    except Exception as e:
        logger.error("Unable to load cache : %s", e)

    for sentence in nltk.sent_tokenize(text):
        if sentence.lower() not in cache:
            logger.info("Unable to get ''%s'' from cache", sentence)
            break

        logger.debug("Cache   to audio : %s", sentence)
        audio_array = cache[sentence.lower()]
        yield np.concatenate([audio_array, silence])


def generate_audio_to_cache(text: str, language: str) -> None:
    """
    For background task : Only convert text to audio, and save audio content in cache.
    """
    voice_preset = f"v2/{language}_speaker_2"
    cache_file = f"/shared/tts_cache/{voice_preset}.json"
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)

    cache = {}
    try:
        with open(cache_file, "rb") as f:
            cache = dict(np.load(f))
    except Exception as e:
        logger.error("Unable to load cache : %s", e)

    for i, sentence in enumerate(nltk.sent_tokenize(text)):
        if sentence.lower() in cache:
            continue

        logger.debug("Convert to audio : %s", sentence)
        audio_array = sentense_to_audio(sentence, voice_preset)
        cache[sentence.lower()] = audio_array

        if i % 10 == 9:
            with open(cache_file, "wb+") as f:
                np.savez_compressed(f, **cache)

    with open(cache_file, "wb+") as f:
        np.savez_compressed(f, **cache)


def generate_audio(text: str, language: str) -> None:
    voice_preset = f"v2/{language}_speaker_2"
    silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence

    for sentence in nltk.sent_tokenize(text):
        logger.debug("Convert to audio : %s", sentence)
        audio_array = sentense_to_audio(sentence, voice_preset)
        yield np.concatenate([audio_array, silence])


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
