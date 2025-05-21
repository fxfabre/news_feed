from pathlib import Path

import numpy as np
from bark import SAMPLE_RATE
from scipy.io.wavfile import write as write_wav

from tts_api.controllers.tts_controller import generate_audio


async def tts_on_text_files():
    # web_url_file = Path("/shared/text_files/web_urls.txt")

    for file_path in Path("/shared/text_files").glob("*.txt"):
        wav_path = file_path.with_suffix(".wav")
        content = file_path.read_text()
        audio_parts = generate_audio(content, "fr")
        write_wav(wav_path, SAMPLE_RATE, np.concatenate(audio_parts))
