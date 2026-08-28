# Voice Commands & Smart Editing

## Objective
Allow users to control their operating system and manipulate text using specific voice triggers, identical to Wispr Flow's command mode.

## Architecture

### 1. Action Classification
Before the transcription is sent to the keyboard for typing, the system will analyze the string for specific trigger phrases.
- **Trigger Format:** `[Command Word] + [Action]`
- **Examples:**
  - "Command Undo" -> Triggers `Ctrl + Z`
  - "Delete that" -> Triggers multiple `Backspace` events to clear the last dictated sentence.
  - "Press Enter" -> Triggers the `Enter` key.

### 2. Custom Voice Macros
Users should be able to define their own shortcuts.
- **Storage:** Macros will be saved in a local `macros.json` file.
- **Structure:** `{"trigger_phrase": "output_text_or_action"}`
- **Execution:** If a transcript exactly matches or starts with a `trigger_phrase`, the `keyboard_manager.py` bypasses standard typing and executes the mapped macro.

## Upcoming Tasks
- [ ] Build the `CommandRouter` in `main.py` to intercept texts before they hit the keyboard.
- [ ] Map standard OS commands (Undo, Redo, Enter, Tab) using the `keyboard` library.
- [ ] Add a JSON parser to load custom user macros into memory on startup.
