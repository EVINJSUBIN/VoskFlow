# VoskFlow 🎙️⌨️

**Vision:** An offline, on-device, privacy-first alternative to Wispr Flow. It runs entirely on your local machine using a Vosk speech recognition model, allowing you to dictate text seamlessly into any application using a global hotkey.

## Core Features
- **Zero-Latency Offline Dictation:** Uses `vosk-api` for incredibly fast, local transcription (no cloud API keys, 100% privacy).
- **Global Hotkey:** Press and hold `Ctrl + Space` (or a custom shortcut) to start listening. Release to instantly type the text into whatever app is currently focused.
- **Auto-Typer:** Simulates native keyboard events to inject the transcribed text seamlessly into Discord, VSCode, Chrome, or any active window.

## Stardance Scorecard Strategy
- **Originality (9/9):** Building a local hardware-integrated OS utility rather than just another web app.
- **Technicality (9/9):** Processing raw microphone streams, handling background threads for OS-level hotkeys, and implementing local ML models (Vosk).
- **Usability (9/9):** It genuinely solves a productivity problem and works universally across Windows.
- **Storytelling:** Devlog focus will be on the challenges of multithreading (audio recording vs. UI/Hotkey listening) and simulating keypresses accurately.

## Implementation Plan (Python Stack)
1. **Setup:** Install Python dependencies (`vosk`, `pyaudio`, `keyboard`).
2. **Audio Pipeline:** Write a script that captures the microphone stream via `pyaudio` and feeds it to a loaded `vosk` model.
3. **OS Integration:** Use the `keyboard` library to listen for a global hotkey to toggle the recording state.
4. **Output:** Once Vosk returns a recognized string, use `keyboard.write()` to type it out.

## Devlogs
### [Day 1] - Scaffolding the Wispr Flow Experience
Today was all about nailing the UI/UX before hooking up the heavy ML models. If this is going to replace the keyboard, it needs to feel native, completely unobtrusive, and incredibly responsive.

*   **The Framework Pivot:** We started by scaffolding a basic popup in `tkinter`, but quickly hit a wall. Tkinter couldn't produce the sleek, anti-aliased, glassmorphic look needed to mimic Wispr Flow. We ripped it out and upgraded the entire stack to **PyQt6**.
*   **Audio-Reactive Waveform:** Instead of static "Listening..." text, we built a custom `QPainter` widget that renders a 7-bar audio waveform. We hooked up `pyaudio` and `numpy` in a background thread to calculate the RMS volume of the microphone in real-time. Now, the waveform physically dances to the user's voice at 60fps, with a subtle sine-wave idle ripple.
*   **Black Glassmorphism:** We initially experimented with native Windows `ctypes` for acrylic blur, but it caused jagged edge clipping on the border radius. We solved this by engineering a pure CSS faux-glass gradient (`rgba(35, 35, 35, 245)`) that perfectly simulates a frosted dark pill.
*   **OS Integration:** It's no longer just a terminal script. It runs as a background daemon in the System Tray. Right-clicking opens a full Desktop Dashboard where users can dynamically remap their Push-To-Talk hotkey, view their transcription history, and customize the color of the waveform animation.

**Next Up:** Wiring the live PyAudio stream directly into the Vosk model for actual offline transcription!

### [Update] - Landing Page is Live fr 🚀
Ngl, the landing page we just dropped absolutely ate and left no crumbs. Added screenshots of our black glassmorphism pill and the bouncing voice bubbles, and the aesthetic is heavily based. Wispr Flow is literally shaking rn. No cap, the UI is serving looks. Now that the site is up, we’re ready to plug in the Vosk ML model and actually let it cook. Huge W. 🔥
