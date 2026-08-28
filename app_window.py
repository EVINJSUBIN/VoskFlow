from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QListWidget, QComboBox, 
                               QStackedWidget, QFrame)
from PyQt6.QtCore import Qt
from datetime import datetime

class AppWindow(QWidget):
    """The main desktop application window for VoskFlow containing History and Settings."""
    def __init__(self, current_hotkey, current_color, on_settings_saved):
        super().__init__()
        self.on_settings_saved = on_settings_saved
        
        self.setWindowTitle("VoskFlow Dashboard")
        self.setFixedSize(600, 400)
        
        # Deep dark desktop app theme
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #EEEEEE;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QListWidget {
                background-color: #1E1E1E;
                border: 1px solid #333333;
                border-radius: 6px;
                padding: 5px;
                font-size: 13px;
                outline: 0;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #2A2A2A;
            }
            QListWidget::item:selected {
                background-color: #2D2D2D;
            }
            QLineEdit, QComboBox {
                background-color: #1E1E1E;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                color: white;
            }
            QPushButton {
                background-color: #007ACC;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0098FF;
            }
            #Sidebar {
                background-color: #1A1A1A;
                border-right: 1px solid #333333;
            }
            #SidebarButton {
                background-color: transparent;
                text-align: left;
                padding: 12px 20px;
                font-size: 15px;
                font-weight: normal;
                border-radius: 0px;
            }
            #SidebarButton:hover {
                background-color: #2A2A2A;
            }
            #SidebarButton:checked {
                background-color: #2D2D2D;
                border-left: 3px solid #007ACC;
                font-weight: bold;
            }
        """)
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- SIDEBAR ---
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(160)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 0)
        sidebar_layout.setSpacing(5)
        
        self.btn_history = QPushButton("📋 History")
        self.btn_history.setObjectName("SidebarButton")
        self.btn_history.setCheckable(True)
        self.btn_history.setChecked(True)
        
        self.btn_settings = QPushButton("⚙️ Settings")
        self.btn_settings.setObjectName("SidebarButton")
        self.btn_settings.setCheckable(True)
        
        sidebar_layout.addWidget(self.btn_history)
        sidebar_layout.addWidget(self.btn_settings)
        sidebar_layout.addStretch()
        
        # --- CONTENT AREA ---
        self.stack = QStackedWidget()
        
        # Page 1: History
        page_history = QWidget()
        history_layout = QVBoxLayout(page_history)
        history_layout.setContentsMargins(20, 20, 20, 20)
        
        title_history = QLabel("Dictation History")
        title_history.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        history_layout.addWidget(title_history)
        
        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)
        
        # Page 2: Settings
        page_settings = QWidget()
        settings_layout = QVBoxLayout(page_settings)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        
        title_settings = QLabel("Configuration")
        title_settings.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        settings_layout.addWidget(title_settings)
        
        # Hotkey Setting
        settings_layout.addWidget(QLabel("Push-To-Talk Hotkey:"))
        self.hotkey_input = QLineEdit(current_hotkey)
        settings_layout.addWidget(self.hotkey_input)
        
        settings_layout.addSpacing(15)
        
        # Color Setting
        settings_layout.addWidget(QLabel("Waveform Color:"))
        self.color_combo = QComboBox()
        self.colors = {
            "White (Classic)": "#FFFFFF",
            "Wispr Orange": "#FF6B00",
            "Electric Blue": "#00D2FF",
            "Neon Green": "#39FF14",
            "Deep Purple": "#B026FF"
        }
        for name in self.colors.keys():
            self.color_combo.addItem(name)
            
        # Select current color if possible
        for index, (name, hex_val) in enumerate(self.colors.items()):
            if hex_val == current_color:
                self.color_combo.setCurrentIndex(index)
                break
                
        settings_layout.addWidget(self.color_combo)
        
        settings_layout.addStretch()
        
        # Save Button
        save_btn = QPushButton("Apply Settings")
        save_btn.clicked.connect(self._save_settings)
        settings_layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        # Add pages to stack
        self.stack.addWidget(page_history)
        self.stack.addWidget(page_settings)
        
        # Wiring sidebar clicks
        self.btn_history.clicked.connect(lambda: self._switch_tab(0))
        self.btn_settings.clicked.connect(lambda: self._switch_tab(1))
        
        # Assemble Main Layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

    def _switch_tab(self, index):
        self.stack.setCurrentIndex(index)
        self.btn_history.setChecked(index == 0)
        self.btn_settings.setChecked(index == 1)
        
    def _save_settings(self):
        new_hotkey = self.hotkey_input.text()
        selected_name = self.color_combo.currentText()
        new_color = self.colors[selected_name]
        
        if self.on_settings_saved:
            self.on_settings_saved(new_hotkey, new_color)

    def add_history_item(self, text):
        """Adds a transcribed text item to the history list widget."""
        timestamp = datetime.now().strftime("%I:%M %p")
        display_text = f"[{timestamp}] {text}"
        self.history_list.insertItem(0, display_text) # Insert at top
