"""
Wake-word listener using Porcupine.

Runs continuously with a light footprint, listening only for the configured
wake phrase. Full audio capture and transcription only start after a
detection fires, keeping idle CPU/power usage low on the dedicated "brain"
machine Luna runs on.
"""

import struct
import pvporcupine
import pyaudio

from config import PORCUPINE_ACCESS_KEY, WAKE_WORD


class WakeWordListener:
    def __init__(self, access_key: str = PORCUPINE_ACCESS_KEY, keyword: str = WAKE_WORD):
        self.porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=[keyword],
        )
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def start(self):
        self.stream = self.audio.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
        )

    def listen_for_wake(self) -> bool:
        """Blocks until the wake word is detected, then returns True."""
        if self.stream is None:
            self.start()

        while True:
            pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            result = self.porcupine.process(pcm)
            if result >= 0:
                return True

    def close(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.porcupine.delete()
        self.audio.terminate()
