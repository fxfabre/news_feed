import logging
from typing import Iterable
import numpy as np
import spacy
from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse, ORJSONResponse
from spacy.tokens import Span

from tts_api.models.tts_request import TtsRequest
from tts_api.models.wavefile_content import AudioSegment
from transformers import AutoProcessor, AutoModel

logger = logging.getLogger(__name__)
router = APIRouter()
MODEL_NAME = "suno/bark-small"


@router.post("/", response_model=AudioSegment, response_class=ORJSONResponse)
async def generate_speech(body: TtsRequest) -> AudioSegment:
    logger.info("Loading model %s", MODEL_NAME)
    processor = AutoProcessor.from_pretrained(MODEL_NAME, cache_dir="/model")
    model = AutoModel.from_pretrained(MODEL_NAME, cache_dir="/model")
    voice_preset = f"v2/{body.language}_speaker_2"

    # return StreamingResponse(
    #     text_to_audio(processor, model, body.text, voice_preset, body.language),
    #     media_type="text/json"
    # )
    return await text_to_audio(processor, model, body.text, voice_preset, body.language)


async def text_to_audio(processor, model, text: str, voice_preset: str, language: str) -> AudioSegment:
    spacy_model = {
        "fr": "fr_core_news_sm",
        "en": "en_core_web_sm",
    }[language]
    nlp = spacy.load(spacy_model)

    audios: list[dict] = []
    for sentense in nlp(text).sents:
        sentense: Span
        logger.debug("Convert to audio : %s", sentense)
        audio = generate_audio_for(processor, model, sentense.text, voice_preset)
        audios.append(audio)

    if len(audios) == 0:
        return AudioSegment(rate=0, data=[], content_type="audio/wav")

    return AudioSegment(
        rate=audios[0]["rate"],
        data=np.concatenate(audio["data"] for audio in audios),
        content_type="audio/wav"
    )


def generate_audio_for(processor, model, sentense: str, voice_preset: str) -> dict:
    inputs = processor(
        text=sentense,
        voice_preset=voice_preset,
        return_tensors="pt",
    )

    logger.info("Start generating speech using voice preset: %s", voice_preset)
    speech_values = model.generate(**inputs, do_sample=True)
    data = speech_values.cpu().numpy().squeeze()

    logger.info("Speech generation finished. Len: %s, dtype %s", len(data), data.dtype)

    return {
        "rate": model.generation_config.sample_rate,
        "data": data,
    }
