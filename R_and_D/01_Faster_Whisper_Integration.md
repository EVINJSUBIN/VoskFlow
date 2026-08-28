# Faster-Whisper Integration & Live Streaming

## Objective
Replace the standard Vosk backend with `faster-whisper` (CTranslate2) to achieve near human-level accuracy, automatic capitalization, and punctuation, while mimicking Wispr Flow's live dictation responsiveness.

## Architecture

### 1. The Transcription Engine
- **Library:** `faster-whisper`
- **Execution:** Runs optimally on CPU (with INT8 quantization) or GPU (CUDA).
- **Behavior:** Takes raw audio numpy arrays and returns formatted text strings.
- **Why?** Vosk is fast but lacks context. Whisper understands sentence structure, making the output instantly usable in professional environments.

### 2. Live Transcription Streaming
Instead of waiting for the user to release `Ctrl + Space` to begin transcription, the audio pipeline should process chunks continuously.
- **VAD (Voice Activity Detection):** Use `webrtcvad` to detect when the user is speaking.
- **Buffering:** As the user speaks, chunk the audio into 1-2 second rolling buffers.
- **Partial Transcripts:** Feed these buffers to `faster-whisper` to get partial texts.
- **Final Output:** When the hotkey is released, the final transcript is already 90% processed, resulting in zero-latency injection.

## Upcoming Tasks
- [ ] Add `faster-whisper` and `webrtcvad` to dependencies.
- [ ] Create `transcriber.py` module to wrap the WhisperModel.
- [ ] Refactor `audio_engine.py` to stream buffers instead of just calculating volume RMS.
