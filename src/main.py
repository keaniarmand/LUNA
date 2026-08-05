"""
Entry point — runs Luna's core loop:

    wake word -> record until silence -> transcribe -> Claude -> speak
                                                            |
                                                  short-term session memory
"""

from wake_word import WakeWordListener
from transcribe import record_until_silence, transcribe
from reasoning import get_response
from speak import Speaker
from memory import SessionMemory


def run():
    listener = WakeWordListener()
    speaker = Speaker()
    memory = SessionMemory()

    print("Luna is listening for the wake word...")

    try:
        while True:
            listener.listen_for_wake()
            print("Wake word detected — listening...")

            audio_buf = record_until_silence()
            user_input = transcribe(audio_buf)
            print(f"You said: {user_input}")

            if not user_input:
                continue

            reply = get_response(user_input, memory.get_history())
            print(f"Luna: {reply}")

            speaker.say(reply)
            memory.add_exchange(user_input, reply)

    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        listener.close()


if __name__ == "__main__":
    run()
