# Design Notes

## Why this project exists

Luna is built to hold context I'd otherwise have to carry around in my head or reconstruct from scattered notes — across work, projects, and day-to-day decisions. The goal is a voice I can talk to that remembers what I told it, helps me think out loud, and takes a little weight off my plate. Not a replacement for planning or thinking — a partner for it.

This is also intentionally a portfolio piece: a real, working system with documented tradeoffs, not a scripted demo.

## How it should help, day to day

- **A thinking partner** — talking through a decision out loud, the way you'd think out loud with a friend.
- **Less mental overhead** — offloading details so they're not the only place they live.
- **A voice, not a screen** — designed to fit into a day that's already full, without adding another app to check.

## Tradeoffs considered

**Voice-only vs. app/screen.** Chose voice-only deliberately. An app is another thing to open and check; the point of Luna is to reduce that friction, not add to it.

**Whisper API vs. local transcription.** The machine running Luna is intentionally cheap, low-power hardware — running Whisper locally would require compute the hardware doesn't have. API-based transcription trades a network dependency for speed and accuracy without needing local compute muscle.

**Two-machine setup vs. running on a personal laptop.** Running Luna on a dedicated, always-on machine keeps it from competing with day-to-day personal computer use, and keeps the "brain" always listening without needing a personal laptop to stay powered on and unlocked.

**Short-term memory before long-term.** Long-term memory — what's worth remembering, how to retrieve it well, how to avoid it becoming noise — is the harder problem. Getting the core conversational loop solid first means testing memory retrieval against a system that's already reliable, rather than debugging both at once.

## Open questions for phase 2

- What's the right schema for persistent memory — flat facts, categorized entries, something else?
- How much should get written to long-term memory automatically vs. requiring an explicit "remember this"?
- How does retrieval avoid pulling in irrelevant or stale context during a live conversation?
