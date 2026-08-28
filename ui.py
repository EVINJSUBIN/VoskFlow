import math
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QPainter, QColor, QBrush, QGuiApplication

class WaveformWidget(QWidget):
    """A custom widget that renders a Wispr Flow style animated audio waveform."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(68, 30)
        self._target_vol = 0.0
        self._current_vol = 0.0
        self.time_step = 0.0
        # Default wave color (White)
        self.wave_color = QColor(255, 255, 255, 230)
    
    def set_volume(self, vol):
        self._target_vol = vol
    
    def set_color(self, hex_color):
        self.wave_color = QColor(hex_color)
        # Ensure it has a nice slight transparency like the original
        self.wave_color.setAlpha(230)
        self.update()
        
    def update_animation(self):
        self._current_vol += (self._target_vol - self._current_vol) * 0.3
        self.time_step += 0.15 
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        num_bars = 7
        bar_w = 3.0
        spacing = 2.0 # Tighter spacing for a smaller pill
        total_w = (num_bars * bar_w) + ((num_bars - 1) * spacing)
        
        start_x = (self.width() - total_w) / 2
        center_y = self.height() / 2
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.wave_color))
        
        multipliers = [0.3, 0.6, 0.9, 1.0, 0.9, 0.6, 0.3]
        
        for i in range(num_bars):
            idle_wave = math.sin(self.time_step + i * 0.5) * 1.5
            bar_h = 4.0 + idle_wave + (self._current_vol * 18.0 * multipliers[i])
            bar_h = max(3.0, min(bar_h, self.height() - 8))
            
            x = start_x + (i * (bar_w + spacing))
            y = center_y - (bar_h / 2)
            
            painter.drawRoundedRect(int(x), int(y), int(bar_w), int(bar_h), int(bar_w/2), int(bar_w/2))


class DictationUI(QWidget):
    show_signal = pyqtSignal(str)
    hide_signal = pyqtSignal()
    update_status_signal = pyqtSignal(str)
    volume_signal = pyqtSignal(float)
    color_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
        
        self.show_signal.connect(self._show_ui)
        self.hide_signal.connect(self._hide_ui)
        self.update_status_signal.connect(self._set_status)
        self.volume_signal.connect(self._update_volume)
        self.color_signal.connect(self._update_color)
        
    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnTopHint | 
                            Qt.WindowType.Tool)
        
        # Required for perfect anti-aliased rounded corners without OS black edges
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        pill_width = 68
        pill_height = 30
        self.setFixedSize(pill_width, pill_height)
        
        self.container = QWidget(self)
        self.container.setObjectName("PillContainer")
        self.container.setGeometry(0, 0, pill_width, pill_height)
        
        # High quality CSS faux-glass (Deep Black Gradient). 
        # This completely solves the jagged edge artifacting caused by the Windows ctypes blur API.
        self.container.setStyleSheet(f"""
            QWidget#PillContainer {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                            stop:0 rgba(35, 35, 35, 245), 
                                            stop:1 rgba(15, 15, 15, 245));
                border-radius: {pill_height // 2}px; 
                border: 1px solid rgba(255, 255, 255, 20);
            }}
        """)
        
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.wave_widget = WaveformWidget(self)
        layout.addWidget(self.wave_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Bottom placement
        screen_geo = QGuiApplication.primaryScreen().availableGeometry()
        x = (screen_geo.width() - self.width()) // 2
        y = screen_geo.bottom() - self.height() - 20 
        self.move(x, y)
        
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.wave_widget.update_animation)
        self.anim_timer.start(16) 
        
    def _show_ui(self, text):
        self.show()
        
    def _hide_ui(self):
        self.hide()
        
    def _set_status(self, text):
        pass
        
    def _update_volume(self, vol):
        self.wave_widget.set_volume(vol)
        
    def _update_color(self, hex_color):
        self.wave_widget.set_color(hex_color)
