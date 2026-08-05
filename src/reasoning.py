"""
Reasoning layer — sends transcribed input plus recent conversation history
to the Claude API and returns a spoken-friendly response.
"""

import anthropic

from config import ANTHROPIC_API_KEY, CLAUDE_MODEL

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """\
You are Luna, a personal voice assistant. You speak out loud, so keep \
responses short, natural, and conversational — no markdown, no bullet \
points, no lists read aloud. Get to the point in a sentence or two unless \
the person clearly wants to think through something longer with you.
"""


def get_response(user_input: str, session_memory: list[dict]) -> str:
    """
    Sends the user's transcribed input plus session history to Claude
    and returns the text response to be spoken back.
    """
    messages = session_memory + [{"role": "user", "content": user_input}]

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    reply_text = "".join(
        block.text for block in response.content if block.type == "text"
    )
    return reply_text.strip()
