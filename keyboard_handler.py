import keyboard
import time

class KeyboardManager:
    def __init__(self, hotkey="ctrl+space", on_press_callback=None, on_release_callback=None):
        self.on_press_callback = on_press_callback
        self.on_release_callback = on_release_callback
        self.is_recording = False
        self.keys = []
        self.set_hotkey(hotkey)
        
    def set_hotkey(self, hotkey_str):
        """Dynamically update the push-to-talk hotkey."""
        # Split by '+' and clean up whitespace
        self.keys = [k.strip().lower() for k in hotkey_str.split('+')]
        print(f"[KeyboardManager] Hotkey updated to: {self.keys}")
        
    def start_listening(self):
        """Registers a global hook to detect Push-to-Talk via the parsed hotkey."""
        keyboard.hook(self._keyboard_event)
        
    def _keyboard_event(self, event):
        """Internal callback for all keyboard events to detect our hotkey state."""
        if not self.keys: return
        
        # Check if ALL keys in our designated combo are currently held down
        all_pressed = all(keyboard.is_pressed(k) for k in self.keys)
        
        if all_pressed:
            if not self.is_recording:
                self.is_recording = True
                if self.on_press_callback: self.on_press_callback()
        elif self.is_recording:
            # If we were recording but the combo is broken (user released at least one key)
            self.is_recording = False
            if self.on_release_callback: self.on_release_callback()
                
    def type_text(self, text):
        """Simulates keyboard typing to inject the transcribed text."""
        # A short sleep helps ensure the hotkey is fully released
        # before we start typing, preventing accidental triggers of other OS shortcuts.
        time.sleep(0.1)
        keyboard.write(text)
