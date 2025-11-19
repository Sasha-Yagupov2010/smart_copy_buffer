import sys
import keyboard
import pyperclip
import time
import os
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, 
                               QLabel, QFrame, QMessageBox, QProgressBar, QCheckBox)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QPalette, QColor

# Константы
MAX_HISTORY_SIZE = 100
HISTORY_FILE = "clipboard_history.txt"

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(200)
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

class ClipboardManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.clipboard_history = []
        self.last_clipboard_content = ""
        self.is_dark_theme = True
        self.setup_ui()
        self.load_history()
        self.setup_clipboard_monitor()
        self.setup_hotkeys()
        self.update_display()
        
    def setup_ui(self):
        self.setWindowTitle("Clipboard Manager Pro")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(700, 500)
        
        self.apply_theme()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Заголовок и переключатель темы
        header_layout = QHBoxLayout()
        
        title = QLabel("📋 Clipboard Manager")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.theme_toggle = QCheckBox("Тёмная тема")
        self.theme_toggle.setChecked(True)
        self.theme_toggle.toggled.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_toggle)
        
        layout.addLayout(header_layout)
        
        # Статистика
        self.stats_label = QLabel("Записей: 0")
        self.stats_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.stats_label)
        
        # История
        history_label = QLabel("📜 История:")
        layout.addWidget(history_label)
        
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.history_list)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.copy_all_btn = AnimatedButton("📋 Копировать всю историю")
        self.copy_all_btn.clicked.connect(self.copy_all_history)
        buttons_layout.addWidget(self.copy_all_btn)
        
        self.clear_btn = AnimatedButton("🗑️ Очистить историю")
        self.clear_btn.clicked.connect(self.clear_history_confirmation)
        buttons_layout.addWidget(self.clear_btn)
        
        layout.addLayout(buttons_layout)
        
        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(MAX_HISTORY_SIZE)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # Статус
        self.status_label = QLabel("Готов к работе...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
    def apply_theme(self):
        if self.is_dark_theme:
            # Тёмно-синяя тема
            self.setStyleSheet("""
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
            """)
        else:
            # Светло-синяя тема
            self.setStyleSheet("""
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
            """)
    
    def toggle_theme(self):
        self.is_dark_theme = self.theme_toggle.isChecked()
        self.apply_theme()
    
    def setup_clipboard_monitor(self):
        """Настраивает мониторинг буфера обмена в реальном времени"""
        self.clipboard_timer = QTimer()
        self.clipboard_timer.timeout.connect(self.check_clipboard)
        self.clipboard_timer.start(300)  # Проверка каждые 300 мс
    
    def setup_hotkeys(self):
        """Настраивает глобальные горячие клавиши"""
        try:
            # Отключаем все предыдущие хоткеи
            keyboard.unhook_all()
            
            # Добавляем новые
            keyboard.add_hotkey('ctrl+c', self.on_copy_safe)
            keyboard.add_hotkey('ctrl+1', self.copy_all_history)
            keyboard.add_hotkey('ctrl+2', self.show_stats)
            keyboard.add_hotkey('ctrl+0', self.clear_history_confirmation)
            self.show_status("Горячие клавиши активированы", "success")
        except Exception as e:
            self.show_status(f"Ошибка горячих клавиш: {e}", "error")
    
    def check_clipboard(self):
        """Проверяет изменения в буфере обмена"""
        try:
            current = pyperclip.paste()
            if current != self.last_clipboard_content:
                self.last_clipboard_content = current
        except Exception as e:
            pass
    
    def on_copy_safe(self):
        """Безопасный обработчик копирования"""
        try:
            # Имитируем оригинальное поведение Ctrl+C
            keyboard.send('ctrl+c')
            time.sleep(0.05)  # Небольшая задержка для гарантии копирования
            
            text = pyperclip.paste()
            
            if not text or not text.strip():
                return
                
            # Проверка на дубликат
            if self.clipboard_history and text == self.clipboard_history[-1]:
                return
            
            self.clipboard_history.append(text)
            
            # Ограничение размера истории
            if len(self.clipboard_history) > MAX_HISTORY_SIZE:
                self.clipboard_history.pop(0)
            
            self.save_history()
            self.update_display()
            self.show_status(f"Добавлено: {text[:30]}...", "success")
            
        except Exception as e:
            self.show_status(f"Ошибка: {e}", "error")
    
    def load_history(self):
        try:
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.clipboard_history = [line.strip() for line in f.readlines()]
            self.show_status(f"Загружено {len(self.clipboard_history)} записей", "success")
        except Exception as e:
            self.show_status(f"Ошибка загрузки: {e}", "error")
            self.clipboard_history = []
    
    def save_history(self):
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                for item in self.clipboard_history:
                    f.write(item + '\n')
        except Exception as e:
            self.show_status(f"Ошибка сохранения: {e}", "error")
    
    def on_item_double_clicked(self, item):
        """Копирует выбранный элемент обратно в буфер обмена"""
        text = item.text()
        pyperclip.copy(text)
        self.show_status("Текст скопирован в буфер", "success")
    
    def copy_all_history(self):
        if not self.clipboard_history:
            self.show_status("История пуста", "warning")
            return
        
        # Склеиваем без лишних пробелов
        text_to_copy = "\n".join(self.clipboard_history)
        pyperclip.copy(text_to_copy)
        self.show_status(f"Скопировано {len(self.clipboard_history)} записей", "success")
    
    def clear_history_confirmation(self):
        reply = QMessageBox.question(self, 'Подтверждение', 
                                   'Очистить всю историю?',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.clear_history()
    
    def clear_history(self):
        self.clipboard_history.clear()
        self.save_history()
        self.update_display()
        self.show_status("История очищена", "success")
    
    def show_stats(self):
        stats_text = f"""
=== Статистика ===
Всего записей: {len(self.clipboard_history)}
Максимальный размер: {MAX_HISTORY_SIZE}
"""
        if self.clipboard_history:
            stats_text += "Последние записи:\n"
            last_three = self.clipboard_history[-3:]
            for i, text in enumerate(reversed(last_three)):
                stats_text += f"  {i+1}. {text[:40]}...\n" if len(text) > 40 else f"  {i+1}. {text}\n"
        else:
            stats_text += "  История пуста\n"
        
        QMessageBox.information(self, "Статистика", stats_text)
    
    def update_display(self):
        self.history_list.clear()
        for item in reversed(self.clipboard_history):
            list_item = QListWidgetItem(item)
            self.history_list.addItem(list_item)
        
        count = len(self.clipboard_history)
        self.stats_label.setText(f"📊 Записей: {count}/{MAX_HISTORY_SIZE}")
        self.progress_bar.setValue(count)
        self.progress_bar.setFormat(f"{count}/{MAX_HISTORY_SIZE}")
    
    def show_status(self, message, type="info"):
        colors = {
            "success": "#4CAF50",
            "error": "#F44336", 
            "warning": "#FF9800",
            "info": "#2196F3"
        }
        
        color = colors.get(type, "#2196F3")
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        
        QTimer.singleShot(3000, lambda: self.status_label.setText("Готов..."))
    
    def closeEvent(self, event):
        """Корректное закрытие приложения"""
        self.save_history()
        try:
            keyboard.unhook_all()
        except:
            pass
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Устанавливаем стиль приложения
    app.setStyle('Fusion')
    
    window = ClipboardManager()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
    
