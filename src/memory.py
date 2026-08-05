"""
Short-term session memory.

Holds recent exchanges in memory for the duration of a session so Luna
isn't starting fresh every sentence. Long-term memory (a persistent store
that survives across sessions) is planned for phase 2 — see ROADMAP.md.
"""


class SessionMemory:
    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self._history: list[dict] = []

    def add_exchange(self, user_input: str, assistant_reply: str):
        self._history.append({"role": "user", "content": user_input})
        self._history.append({"role": "assistant", "content": assistant_reply})
        # Keep the window bounded so context doesn't grow unbounded in a long session.
        overflow = len(self._history) - (self.max_turns * 2)
        if overflow > 0:
            self._history = self._history[overflow:]

    def get_history(self) -> list[dict]:
        return list(self._history)

    def clear(self):
        self._history = []
