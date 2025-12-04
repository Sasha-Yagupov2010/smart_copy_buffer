# Константы и настройки приложения
MAX_HISTORY_SIZE = 100
HISTORY_FILE = "clipboard_history.txt"
SCRIPT_BINDINGS_FILE = "script_bindings.json"

# Настройки тем
DARK_THEME_STYLESHEET = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #1e3c72, stop:1 #2a5298);
    }
    QTabWidget::pane {
        border: 1px solid rgba(255, 255, 255, 50);
        background: rgba(255, 255, 255, 20);
        border-radius: 8px;
    }
    QTabBar::tab {
        background: rgba(255, 255, 255, 30);
        border: 1px solid rgba(255, 255, 255, 50);
        padding: 8px 12px;
        margin: 2px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        color: white;
        font-weight: bold;
    }
    QTabBar::tab:selected {
        background: rgba(74, 144, 226, 150);
    }
    QGroupBox {
        border: 2px solid rgba(255, 255, 255, 50);
        border-radius: 8px;
        margin-top: 10px;
        padding-top: 10px;
        color: white;
        font-weight: bold;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 5px;
        background: transparent;
    }
    QTextEdit, QLineEdit {
        background: rgba(255, 255, 255, 20);
        border: 2px solid rgba(255, 255, 255, 50);
        border-radius: 6px;
        padding: 5px;
        color: white;
        font-size: 12px;
    }
    QComboBox {
        background: rgba(255, 255, 255, 20);
        border: 2px solid rgba(255, 255, 255, 50);
        border-radius: 6px;
        padding: 5px;
        color: white;
    }
    QComboBox::drop-down {
        border: none;
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
    QTabWidget::pane {
        border: 1px solid #90caf9;
        background: white;
        border-radius: 8px;
    }
    QTabBar::tab {
        background: #f5f5f5;
        border: 1px solid #90caf9;
        padding: 8px 12px;
        margin: 2px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        color: #333;
        font-weight: bold;
    }
    QTabBar::tab:selected {
        background: #2196f3;
        color: white;
    }
    QGroupBox {
        border: 2px solid #90caf9;
        border-radius: 8px;
        margin-top: 10px;
        padding-top: 10px;
        color: #333;
        font-weight: bold;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 5px;
        background: transparent;
    }
    QTextEdit, QLineEdit {
        background: white;
        border: 2px solid #90caf9;
        border-radius: 6px;
        padding: 5px;
        color: #333;
        font-size: 12px;
    }
    QComboBox {
        background: white;
        border: 2px solid #90caf9;
        border-radius: 6px;
        padding: 5px;
        color: #333;
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