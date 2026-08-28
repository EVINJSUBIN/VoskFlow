import sys
import time
import threading
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter, QBrush

from ui import DictationUI
from keyboard_handler import KeyboardManager
from audio_engine import AudioEngine
from app_window import AppWindow
from stt_engine import STTEngine

def create_tray_icon():
    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor(0, 0, 0, 0)) 
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QBrush(QColor(0, 122, 204)))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(4, 4, 56, 56)
    painter.end()
    
    return QIcon(pixmap)

class AppController(QObject):
    def __init__(self):
        super().__init__()
        
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        self.ui = DictationUI()
        self.audio_engine = AudioEngine(volume_callback=self.on_audio_volume)
        
        # Initialize the actual STT Engine (Faster-Whisper)
        self.stt_engine = STTEngine(model_size="base.en")
        
        self.current_hotkey = "ctrl+space"
        self.current_color = "#FFFFFF" 
        
        self.app_window = AppWindow(
            self.current_hotkey, 
            self.current_color,
            self.on_settings_saved
        )
        
        self.keyboard_manager = KeyboardManager(
            hotkey=self.current_hotkey,
            on_press_callback=self.on_hotkey_press,
            on_release_callback=self.on_hotkey_release
        )
        self.keyboard_manager.start_listening()
        self.is_streaming = False
        
        self.setup_system_tray()
        
        print("VoskFlow started.")
        print("Check your system tray (near the clock) to open the Dashboard.")

    def setup_system_tray(self):
        self.tray_icon = QSystemTrayIcon(create_tray_icon(), self.app)
        self.tray_icon.setToolTip("VoskFlow")
        
        menu = QMenu()
        
        dashboard_action = menu.addAction("Open Dashboard")
        dashboard_action.triggered.connect(self.app_window.show)
        
        menu.addSeparator()
        
        quit_action = menu.addAction("Quit VoskFlow")
        quit_action.triggered.connect(self.quit_app)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def run(self):
        sys.exit(self.app.exec())
        
    def on_settings_saved(self, new_hotkey, new_color):
        if new_hotkey != self.current_hotkey:
            self.current_hotkey = new_hotkey
            self.keyboard_manager.set_hotkey(new_hotkey)
            
        if new_color != self.current_color:
            self.current_color = new_color
            self.ui.color_signal.emit(new_color)
            
        print(f"Settings saved: Hotkey='{new_hotkey}', Color='{new_color}'")

    def quit_app(self):
        print("Quitting VoskFlow...")
        self.audio_engine.stop()
        self.app.quit()

    def on_hotkey_press(self):
        self.ui.show_signal.emit("")
        self.audio_engine.start()
        self.is_streaming = True
        
        # Start Live Streaming worker to keep model warm and process partials
        threading.Thread(target=self._live_stream_worker, daemon=True).start()

    def _live_stream_worker(self):
        """Background thread to transcribe partial audio while hotkey is held."""
        while self.is_streaming:
            time.sleep(0.5) # Process chunks every 500ms
            audio = self.audio_engine.get_current_audio_float32()
            if len(audio) > 16000 * 0.5: 
                # Transcribing partial audio warms up the Whisper cache/KV states
                # and drastically reduces latency upon release.
                partial_text = self.stt_engine.transcribe_audio(audio)
                if partial_text:
                    print(f"Live partial: {partial_text}", end='\r')

    def on_hotkey_release(self):
        self.is_streaming = False
        self.audio_engine.stop()
        
        def process_final():
            # Retrieve the complete audio buffer
            audio_data = self.audio_engine.get_current_audio_float32()
            
            # Final transcription
            final_text = self.stt_engine.transcribe_audio(audio_data)
            
            self.ui.hide_signal.emit()
            
            if final_text:
                print(f"\nFinal transcribed: {final_text}")
                # Type the text natively
                self.keyboard_manager.type_text(final_text + " ")
                # Log to history
                self.app_window.add_history_item(final_text.strip())
            
        threading.Thread(target=process_final, daemon=True).start()

    def on_audio_volume(self, vol):
        self.ui.volume_signal.emit(vol)

if __name__ == "__main__":
    controller = AppController()
    controller.run()
