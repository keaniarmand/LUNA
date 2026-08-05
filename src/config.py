"""
Central config — loads API keys and tunables from environment variables.
Copy .env.example to .env and fill in real values before running.
"""

import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY", "")

CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
WAKE_WORD = os.getenv("WAKE_WORD", "porcupine")  # swap for a custom keyword file later
SILENCE_TIMEOUT_MS = int(os.getenv("SILENCE_TIMEOUT_MS", "1200"))
