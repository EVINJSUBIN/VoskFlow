# Language & Model Manager Settings

## Objective
Wispr Flow supports 100+ languages. To match this locally, we need to allow users to easily download, select, and manage different AI models tailored to their language and hardware capabilities.

## Architecture

### 1. PyQt6 Settings UI Expansion
The current `app_window.py` only handles hotkeys and waveform colors. We will add a new tab: **"Models & Languages"**.

### 2. Model Recommendations Engine
Different users have different needs. The UI should recommend models based on use-case:
- **English Only (Fastest):** `distil-whisper-en` or `base.en`. Requires minimal RAM, lightning fast.
- **Multilingual (High Accuracy):** `whisper-large-v3-turbo` or `small`. Requires more RAM, supports auto-detection of 100+ languages.
- **Hardware Profiling:** On boot, the app will check for a CUDA-compatible GPU. If found, it recommends heavier models. If integrated graphics/CPU, it recommends quantized `base` models.

### 3. Dynamic Loading
- When a user changes the language setting, the app should hot-swap the Whisper model in the background without requiring a full app restart.
- Include a visual progress bar in the UI when a model is being downloaded from HuggingFace for the first time.

## Upcoming Tasks
- [ ] Add the `QComboBox` for Model Selection in `app_window.py`.
- [ ] Write a background downloader thread to fetch `.bin` files without freezing the UI.
- [ ] Implement CUDA vs CPU auto-detection.
