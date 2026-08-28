# Algorithmic Filler Word Removal

## Objective
Remove hesitation markers ("ums", "ahs", "uhs") from the final dictation without relying on a slow, resource-heavy local LLM. Wispr Flow uses LLMs for this, but we can achieve similar results algorithmically for 0ms latency.

## Architecture

### 1. NLP Regex Engine
- A dedicated Python module (`text_processor.py`) that executes immediately after `faster-whisper` returns the text, but before it reaches `keyboard_handler.py`.
- **Pattern Matching:** Use robust regex boundaries to catch isolated filler words.
  - *Example Pattern:* `(?i)\b(um|uh|ah|like|you know)\b`
  
### 2. Post-Cleaning Formatting
When a filler word is removed, it often leaves behind double spaces or stranded punctuation (e.g., "Hello, um, world" -> "Hello, , world").
- **Cleanup Passes:**
  1. Remove floating commas or periods.
  2. Collapse multiple spaces into a single space.
  3. Ensure the sentence retains correct capitalization if a starting filler word is removed.

## Upcoming Tasks
- [ ] Compile a comprehensive list of English filler words.
- [ ] Build the `clean_fillers(text)` function using `re` module.
- [ ] Write unit tests to ensure words containing "um" (like "umbrella") are not accidentally modified.
