"""
Speech-to-text via the Whisper API.

Records audio after the wake word triggers, stops on silence, and sends
the clip to Whisper for transcription. Runs via API rather than locally —
the "brain" machine is intentionally low-power, so this trades a network
dependency for speed and accuracy without needing local compute muscle.
"""

import io
import wave

import pyaudio
import webrtcvad
from openai import OpenAI

from config import OPENAI_API_KEY, SILENCE_TIMEOUT_MS

client = OpenAI(api_key=OPENAI_API_KEY)

SAMPLE_RATE = 16000
FRAME_MS = 30
FRAME_SIZE = int(SAMPLE_RATE * FRAME_MS / 1000)


def record_until_silence(silence_timeout_ms: int = SILENCE_TIMEOUT_MS) -> bytes:
    """Records audio from the mic until `silence_timeout_ms` of silence is detected."""
    vad = webrtcvad.Vad(2)  # aggressiveness 0-3; 2 is a reasonable middle ground
    audio = pyaudio.PyAudio()
    stream = audio.open(
        rate=SAMPLE_RATE,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=FRAME_SIZE,
    )

    frames = []
    silence_ms = 0

    try:
        while True:
            frame = stream.read(FRAME_SIZE, exception_on_overflow=False)
            frames.append(frame)
            is_speech = vad.is_speech(frame, SAMPLE_RATE)
            silence_ms = 0 if is_speech else silence_ms + FRAME_MS
            if silence_ms >= silence_timeout_ms and len(frames) > 10:
                break
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

    return _frames_to_wav_bytes(frames, audio)


def _frames_to_wav_bytes(frames, audio) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # paInt16 = 2 bytes
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(frames))
    buf.seek(0)
    buf.name = "audio.wav"  # Whisper API needs a filename hint
    return buf


def transcribe(audio_buf) -> str:
    """Sends a recorded clip to Whisper and returns the transcribed text."""
    result = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_buf,
    )
    return result.text.strip()
