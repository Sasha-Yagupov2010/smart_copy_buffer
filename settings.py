# Константы и настройки приложения
MAX_HISTORY_SIZE = 100
HISTORY_FILE = "clipboard_history.txt"

# Настройки тем
DARK_THEME_STYLESHEET = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #1e3c72, stop:1 #2a5298);
    }
    QListWidget {
        background: rgba(255, 255, 255, 20);
        border: 2px solid rgba(255, 255, 255, 50);
        border-radius: 8px;
        padding: 5px;
        font-size: 12px;
        color: white;
    }
    QListWidget::item {
        background: rgba(255, 255, 255, 30);
        border-radius: 6px;
        padding: 8px;
        margin: 2px;
        color: white;
    }
    QListWidget::item:selected {
        background: rgba(74, 144, 226, 150);
        color: white;
    }
    QListWidget::item:hover {
        background: rgba(255, 255, 255, 50);
    }
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #4a90e2, stop:1 #357abd);
        border: none;
        border-radius: 6px;
        color: white;
        font-weight: bold;
        padding: 8px 12px;
        font-size: 11px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #3a80d2, stop:1 #2a6aad);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #2a70c2, stop:1 #1a5a9d);
    }
    QLabel {
        color: white;
        font-weight: bold;
    }
    QCheckBox {
        color: white;
        font-weight: bold;
    }
    QCheckBox::indicator {
        width: 16px;
        height: 16px;
        border: 2px solid #4a90e2;
        border-radius: 3px;
        background: rgba(255, 255, 255, 30);
    }
    QCheckBox::indicator:checked {
        background: #4a90e2;
    }
    QProgressBar {
        border: 1px solid rgba(255, 255, 255, 50);
        border-radius: 5px;
        background: rgba(255, 255, 255, 20);
        color: white;
    }
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #00b09b, stop:1 #96c93d);
        border-radius: 4px;
    }
"""

LIGHT_THEME_STYLESHEET = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #e3f2fd, stop:1 #bbdefb);
    }
    QListWidget {
        background: white;
        border: 2px solid #90caf9;
        border-radius: 8px;
        padding: 5px;
        font-size: 12px;
        color: #333;
    }
    QListWidget::item {
        background: #f5f5f5;
        border-radius: 6px;
        padding: 8px;
        margin: 2px;
    }
    QListWidget::item:selected {
        background: #2196f3;
        color: white;
    }
    QListWidget::item:hover {
        background: #e3f2fd;
    }
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #2196f3, stop:1 #1976d2);
        border: none;
        border-radius: 6px;
        color: white;
        font-weight: bold;
        padding: 8px 12px;
        font-size: 11px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #1976d2, stop:1 #1565c0);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #1565c0, stop:1 #0d47a1);
    }
    QLabel {
        color: #333;
        font-weight: bold;
    }
    QCheckBox {
        color: #333;
        font-weight: bold;
    }
    QProgressBar {
        border: 1px solid #90caf9;
        border-radius: 5px;
        background: white;
        color: #333;
    }
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #00b09b, stop:1 #96c93d);
        border-radius: 4px;
    }
"""

# Настройки цветов статуса
STATUS_COLORS = {
    "success": "#4CAF50",
    "error": "#F44336", 
    "warning": "#FF9800",
    "info": "#2196F3"
}

# Настройки анимации
ANIMATION_DURATION = 200

# Настройки горячих клавиш
HOTKEYS = {
    'copy': 'ctrl+c',
    'copy_all': 'ctrl+1',
    'show_stats': 'ctrl+2',
    'clear_history': 'ctrl+0'
}

# Настройки мониторинга буфера обмена
CLIPBOARD_CHECK_INTERVAL = 300  # мс
COPY_DELAY = 0.05  # с

# Импорты для класса кнопки
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QRect, Qt

class AnimatedButton(QPushButton):
    """Анимированная кнопка с эффектом нажатия"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(ANIMATION_DURATION)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            original_geometry = self.geometry()
            self._animation.setStartValue(original_geometry)
            self._animation.setEndValue(QRect(
                original_geometry.x() + 2,
                original_geometry.y() + 2,
                original_geometry.width() - 4,
                original_geometry.height() - 4
            ))
            self._animation.start()
        
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._animation.setDirection(QPropertyAnimation.Backward)
            self._animation.start()
        
        super().mouseReleaseEvent(event)

def get_theme_stylesheet(is_dark_theme):
    """Возвращает стиль для выбранной темы"""
    return DARK_THEME_STYLESHEET if is_dark_theme else LIGHT_THEME_STYLESHEET

def get_status_color(message_type):
    """Возвращает цвет для типа сообщения"""
    return STATUS_COLORS.get(message_type, "#2196F3")