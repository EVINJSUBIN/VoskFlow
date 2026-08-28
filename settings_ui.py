from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

class SettingsWindow(QWidget):
    def __init__(self, current_hotkey, on_hotkey_changed):
        super().__init__()
        self.on_hotkey_changed = on_hotkey_changed
        
        self.setWindowTitle("VoskFlow Settings")
        self.setFixedSize(350, 200)
        
        # Sleek dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                color: #EEEEEE;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                background-color: #2D2D2D;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 6px;
                font-size: 14px;
                color: white;
            }
            QPushButton {
                background-color: #007ACC;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0098FF;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        title = QLabel("VoskFlow Configuration")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Hotkey setting
        hotkey_layout = QHBoxLayout()
        hotkey_label = QLabel("Push-To-Talk Hotkey:")
        self.hotkey_input = QLineEdit(current_hotkey)
        self.hotkey_input.setPlaceholderText("e.g. ctrl+space")
        hotkey_layout.addWidget(hotkey_label)
        hotkey_layout.addWidget(self.hotkey_input)
        
        layout.addLayout(hotkey_layout)
        
        layout.addStretch()
        
        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self._save)
        layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
    def _save(self):
        new_hotkey = self.hotkey_input.text()
        if self.on_hotkey_changed:
            self.on_hotkey_changed(new_hotkey)
        self.hide()
