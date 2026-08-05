"""
Text-to-speech output.

Phase 1 uses OS-native TTS (pyttsx3) to keep the loop dependency-light and
fully offline for this stage. A higher-quality voice (ElevenLabs) is
planned for a later phase once the core loop is solid.
"""

import pyttsx3


class Speaker:
    def __init__(self, rate: int = 185, volume: float = 1.0):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

    def say(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()
