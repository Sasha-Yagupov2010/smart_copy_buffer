import sys
import keyboard
import pyperclip
import time
import os
import subprocess
import json
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, 
                               QLabel, QFrame, QMessageBox, QProgressBar, QCheckBox,
                               QTabWidget, QTextEdit, QLineEdit, QGroupBox, QComboBox,
                               QFileDialog, QListWidget, QDialog, QDialogButtonBox)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QPalette, QColor, QTextCursor

# Импорт настроек и классов из settings.py
from settings import *

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

class ScriptManager:
    """Менеджер для запуска файлов по горячим клавишам"""
    
    def __init__(self):
        self.script_bindings = {}
        self.active_hotkeys = set()
        self.load_bindings()
    
    def load_bindings(self):
        """Загружает привязки из файла"""
        try:
            if os.path.exists(SCRIPT_BINDINGS_FILE):
                with open(SCRIPT_BINDINGS_FILE, 'r', encoding='utf-8') as f:
                    self.script_bindings = json.load(f)
            
            # Перерегистрируем все горячие клавиши
            self.register_all_hotkeys()
        except Exception as e:
            print(f"Ошибка загрузки привязок: {e}")
            self.script_bindings = {}
    
    def save_bindings(self):
        """Сохраняет привязки в файл"""
        try:
            with open(SCRIPT_BINDINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.script_bindings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения привязок: {e}")
    
    def register_all_hotkeys(self):
        """Регистрирует все горячие клавиши из загруженных привязок"""
        try:
            # Очищаем все предыдущие хоткеи
            self.unregister_all_hotkeys()
            
            # Регистрируем новые
            for hotkey, file_path in self.script_bindings.items():
                self.register_hotkey(hotkey, file_path)
                
        except Exception as e:
            print(f"Ошибка регистрации горячих клавиш: {e}")
    
    def register_hotkey(self, hotkey, file_path):
        """Регистрирует одну горячую клавишу"""
        try:
            keyboard.add_hotkey(hotkey, lambda: self.execute_file(file_path))
            self.active_hotkeys.add(hotkey)
            return True
        except Exception as e:
            print(f"Ошибка регистрации горячей клавиши {hotkey}: {e}")
            return False
    
    def unregister_hotkey(self, hotkey):
        """Убирает регистрацию горячей клавиши"""
        try:
            if hotkey in self.active_hotkeys:
                keyboard.remove_hotkey(hotkey)
                self.active_hotkeys.remove(hotkey)
            return True
        except Exception as e:
            print(f"Ошибка удаления горячей клавиши {hotkey}: {e}")
            return False
    
    def unregister_all_hotkeys(self):
        """Убирает все зарегистрированные горячие клавиши"""
        try:
            keyboard.unhook_all()
            self.active_hotkeys.clear()
        except Exception as e:
            print(f"Ошибка очистки горячих клавиш: {e}")
    
    def add_binding(self, hotkey, file_path):
        """Добавляет привязку горячей клавиши к файлу"""
        try:
            # Проверяем валидность горячей клавиши
            if not self.is_valid_hotkey(hotkey):
                return False
            
            # Удаляем старую привязку, если была
            if hotkey in self.script_bindings:
                self.unregister_hotkey(hotkey)
            
            # Добавляем новую привязку
            if self.register_hotkey(hotkey, file_path):
                self.script_bindings[hotkey] = file_path
                self.save_bindings()
                return True
            return False
        except Exception as e:
            print(f"Ошибка добавления привязки: {e}")
            return False
    
    def remove_binding(self, hotkey):
        """Удаляет привязку"""
        try:
            if hotkey in self.script_bindings:
                self.unregister_hotkey(hotkey)
                del self.script_bindings[hotkey]
                self.save_bindings()
                return True
            return False
        except Exception as e:
            print(f"Ошибка удаления привязки: {e}")
            return False
    
    def is_valid_hotkey(self, hotkey):
        """Проверяет валидность горячей клавиши"""
        try:
            # Пробуем разобрать горячую клавишу
            keyboard.parse_hotkey(hotkey)
            return True
        except Exception as e:
            print(f"Неверный формат горячей клавиши {hotkey}: {e}")
            return False
    
    def execute_file(self, file_path):
        """Выполняет/открывает файл в новом окне"""
        try:
            if not os.path.exists(file_path):
                print(f"Файл не существует: {file_path}")
                return False
            
            print(f"Запускаем файл: {file_path}")
            
            # Открываем файл в новом процессе
            if os.path.splitext(file_path)[1].lower() in ['.py', '.pyw']:
                # Python скрипты запускаем через интерпретатор
                subprocess.Popen([sys.executable, file_path], 
                                creationflags=subprocess.CREATE_NEW_CONSOLE)
            elif os.path.splitext(file_path)[1].lower() in ['.bat', '.cmd']:
                # BAT файлы тоже в новом окне
                subprocess.Popen([file_path], 
                                creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                # Остальные файлы открываем стандартным способом
                os.startfile(file_path)
            
            print(f"Файл успешно запущен: {file_path}")
            return True
        except Exception as e:
            print(f"Ошибка запуска файла {file_path}: {e}")
            return False
    
    def get_all_bindings(self):
        """Возвращает все привязки"""
        return self.script_bindings


class AddScriptDialog(QDialog):
    """Диалог добавления привязки скрипта"""

    def __init__(self, parent=None, is_dark_theme=True):
        super().__init__(parent)
        self.is_dark_theme = is_dark_theme
        self.setWindowTitle("Добавить привязку файла")
        self.setModal(True)
        self.resize(500, 150)
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Горячая клавиша
        hotkey_layout = QHBoxLayout()
        hotkey_layout.addWidget(QLabel("Горячая клавиша:"))
        self.hotkey_edit = QLineEdit()
        self.hotkey_edit.setPlaceholderText("например: ctrl+alt+1")
        hotkey_layout.addWidget(self.hotkey_edit)
        layout.addLayout(hotkey_layout)

        # Выбор файла
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Файл для запуска:"))
        self.file_edit = QLineEdit()
        self.file_edit.setPlaceholderText("Выберите файл...")
        file_layout.addWidget(self.file_edit)

        self.browse_btn = QPushButton("Обзор...")
        self.browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(self.browse_btn)
        layout.addLayout(file_layout)

        # Кнопки
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def apply_theme(self):
        """Применяет тему к диалогу"""
        self.setStyleSheet(get_theme_stylesheet(self.is_dark_theme))

    def browse_file(self):
        """Открывает диалог выбора файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл для запуска",
            "",
            "All Files (*);;Python Files (*.py);;Batch Files (*.bat);;Executable Files (*.exe)"
        )
        if file_path:
            self.file_edit.setText(file_path)

    def get_data(self):
        """Возвращает данные из диалога"""
        return {
            'hotkey': self.hotkey_edit.text().strip(),
            'file_path': self.file_edit.text().strip()
        }

class ClipboardManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.clipboard_history = []
        self.last_clipboard_content = ""
        self.is_dark_theme = True
        self.script_manager = ScriptManager()
        self.setup_ui()
        self.load_history()
        self.setup_clipboard_monitor()
        self.setup_hotkeys()
        self.update_display()
        self.load_script_bindings()
        
    def setup_ui(self):
        self.setWindowTitle("Clipboard Manager + File Launcher")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(800, 600)
        
        self.apply_theme()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Создаем вкладки
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Вкладка истории буфера обмена
        self.setup_clipboard_tab()
        
        # Вкладка запуска файлов
        self.setup_scripts_tab()
        
    def setup_clipboard_tab(self):
        """Настраивает вкладку буфера обмена"""
        clipboard_tab = QWidget()
        clipboard_layout = QVBoxLayout(clipboard_tab)
        
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
        
        clipboard_layout.addLayout(header_layout)
        
        # Статистика
        self.stats_label = QLabel("Записей: 0")
        self.stats_label.setAlignment(Qt.AlignCenter)
        clipboard_layout.addWidget(self.stats_label)
        
        # История
        history_label = QLabel("📜 История:")
        clipboard_layout.addWidget(history_label)
        
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        clipboard_layout.addWidget(self.history_list)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.copy_all_btn = AnimatedButton("📋 Копировать всю историю")
        self.copy_all_btn.clicked.connect(self.copy_all_history)
        buttons_layout.addWidget(self.copy_all_btn)
        
        self.clear_btn = AnimatedButton("🗑️ Очистить историю")
        self.clear_btn.clicked.connect(self.clear_history_confirmation)
        buttons_layout.addWidget(self.clear_btn)
        
        clipboard_layout.addLayout(buttons_layout)
        
        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(MAX_HISTORY_SIZE)
        self.progress_bar.setTextVisible(True)
        clipboard_layout.addWidget(self.progress_bar)
        
        self.tab_widget.addTab(clipboard_tab, "📋 Буфер обмена")
        
    def setup_scripts_tab(self):
        """Настраивает вкладку запуска файлов"""
        scripts_tab = QWidget()
        scripts_layout = QVBoxLayout(scripts_tab)
        
        # Заголовок
        scripts_title = QLabel("🚀 Запуск файлов по горячим клавишам")
        scripts_title_font = QFont()
        scripts_title_font.setPointSize(16)
        scripts_title_font.setBold(True)
        scripts_title.setFont(scripts_title_font)
        scripts_layout.addWidget(scripts_title)
        
        # Группа управления привязками
        bindings_group = QGroupBox("Привязки файлов к горячим клавишам")
        bindings_layout = QVBoxLayout(bindings_group)
        
        # Кнопки управления привязками
        bindings_buttons_layout = QHBoxLayout()
        
        self.add_binding_btn = AnimatedButton("➕ Добавить привязку")
        self.add_binding_btn.clicked.connect(self.add_script_binding)
        bindings_buttons_layout.addWidget(self.add_binding_btn)
        
        self.remove_binding_btn = AnimatedButton("➖ Удалить привязку")
        self.remove_binding_btn.clicked.connect(self.remove_script_binding)
        bindings_buttons_layout.addWidget(self.remove_binding_btn)
        
        bindings_layout.addLayout(bindings_buttons_layout)
        
        # Список привязок
        self.bindings_list = QListWidget()
        self.bindings_list.setMinimumHeight(300)
        bindings_layout.addWidget(self.bindings_list)
        
        scripts_layout.addWidget(bindings_group)
        
        # Статус
        self.status_label = QLabel("Готов к работе...")
        self.status_label.setAlignment(Qt.AlignCenter)
        scripts_layout.addWidget(self.status_label)
        
        self.tab_widget.addTab(scripts_tab, "🚀 Запуск файлов")
        
    def load_script_bindings(self):
        """Загружает список привязок"""
        self.bindings_list.clear()
        bindings = self.script_manager.get_all_bindings()
        for hotkey, file_path in bindings.items():
            filename = os.path.basename(file_path)
            item_text = f"{hotkey} → {filename}"
            list_item = QListWidgetItem(item_text)
            list_item.setData(Qt.UserRole, hotkey)
            self.bindings_list.addItem(list_item)
    
    def add_script_binding(self):
        """Добавляет новую привязку"""
        dialog = AddScriptDialog(self, False)  # Передаем тему
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            hotkey = data['hotkey']
            file_path = data['file_path']
            
            if not hotkey:
                self.show_status("Введите горячую клавишу", "error")
                return
            
            if not file_path or not os.path.exists(file_path):
                self.show_status("Выберите существующий файл", "error")
                return
            
            if self.script_manager.add_binding(hotkey, file_path):
                self.load_script_bindings()
                self.show_status(f"Привязка добавлена: {hotkey} → {os.path.basename(file_path)}", "success")
            else:
                self.show_status("Ошибка добавления привязки", "error")
    
    def remove_script_binding(self):
        """Удаляет выбранную привязку"""
        current_item = self.bindings_list.currentItem()
        if not current_item:
            self.show_status("Выберите привязку для удаления", "warning")
            return
        
        hotkey = current_item.data(Qt.UserRole)
        if self.script_manager.remove_binding(hotkey):
            self.load_script_bindings()
            self.show_status(f"Привязка удалена: {hotkey}", "success")
        else:
            self.show_status("Ошибка удаления привязки", "error")
    
    def apply_theme(self):
        """Применяет выбранную тему"""
        self.setStyleSheet(get_theme_stylesheet(self.is_dark_theme))
    
    def toggle_theme(self):
        """Переключает тему"""
        self.is_dark_theme = self.theme_toggle.isChecked()
        self.apply_theme()
    
    def setup_clipboard_monitor(self):
        """Настраивает мониторинг буфера обмена в реальном времени"""
        self.clipboard_timer = QTimer()
        self.clipboard_timer.timeout.connect(self.check_clipboard)
        self.clipboard_timer.start(CLIPBOARD_CHECK_INTERVAL)
    
    def setup_hotkeys(self):
        """Настраивает глобальные горячие клавиши"""
        try:
            keyboard.add_hotkey(HOTKEYS['copy'], self.on_copy_safe)
            keyboard.add_hotkey(HOTKEYS['copy_all'], self.copy_all_history)
            keyboard.add_hotkey(HOTKEYS['show_stats'], self.show_stats)
            keyboard.add_hotkey(HOTKEYS['clear_history'], self.clear_history_confirmation)
            self.show_status("Горячие клавиши активированы", "success")
        except Exception as e:
            self.show_status(f"Ошибка горячих клавиш: {e}", "error")
    
    def check_clipboard(self):
        """Проверяет изменения в буфере обмена"""
        try:
            current = pyperclip.paste()
            if current and current != self.last_clipboard_content:
                self.last_clipboard_content = current
        except Exception as e:
            pass
    
    def on_copy_safe(self):
        """Безопасный обработчик копирования"""
        try:
            # Имитируем оригинальное поведение Ctrl+C
            keyboard.send('ctrl+c')
            time.sleep(COPY_DELAY)  # Небольшая задержка для гарантии копирования
            
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
            self.show_status(f"Ошибка копирования: {e}", "error")
    
    def load_history(self):
        """Загружает историю из файла"""
        try:
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.clipboard_history = [line.strip() for line in f.readlines()]
            self.show_status(f"Загружено {len(self.clipboard_history)} записей", "success")
        except Exception as e:
            self.show_status(f"Ошибка загрузки: {e}", "error")
            self.clipboard_history = []
    
    def save_history(self):
        """Сохраняет историю в файл"""
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
        """Копирует всю историю в буфер обмена"""
        if not self.clipboard_history:
            self.show_status("История пуста", "warning")
            return
        
        text_to_copy = "\n".join(self.clipboard_history)
        pyperclip.copy(text_to_copy)
        self.show_status(f"Скопировано {len(self.clipboard_history)} записей", "success")
        
    '''
    def clear_history_confirmation(self):
        """Подтверждение очистки истории"""
        reply = QMessageBox.question(self, 'Подтверждение', 
                                   'Очистить всю историю?',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.clear_history()
    '''
    def clear_history_confirmation(self):
        self.clear_history()            
    
    def clear_history(self):
        """Очищает историю"""
        self.clipboard_history.clear()
        self.save_history()
        self.update_display()
        self.show_status("История очищена", "success")
    
    def show_stats(self):
        """Показывает статистику"""
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
        """Обновляет отображение истории"""
        self.history_list.clear()
        for item in reversed(self.clipboard_history):
            # Обрезаем длинный текст для отображения
            #display_text = item[:100] + "..." if len(item) > 100 else item
            display_text = item
            list_item = QListWidgetItem(display_text)
            list_item.setToolTip(item)  # Полный текст в подсказке
            self.history_list.addItem(list_item)
        
        count = len(self.clipboard_history)
        self.stats_label.setText(f"📊 Записей: {count}/{MAX_HISTORY_SIZE}")
        self.progress_bar.setValue(count)
        self.progress_bar.setFormat(f"{count}/{MAX_HISTORY_SIZE}")
    
    def show_status(self, message, type="info"):
        """Показывает статусное сообщение"""
        color = get_status_color(type)
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

def get_theme_stylesheet(is_dark_theme):
    """Возвращает стиль для выбранной темы"""
    return DARK_THEME_STYLESHEET if is_dark_theme else LIGHT_THEME_STYLESHEET

def get_status_color(message_type):
    """Возвращает цвет для типа сообщения"""
    return STATUS_COLORS.get(message_type, "#2196F3")

def main():
    app = QApplication(sys.argv)
    
    # Устанавливаем стиль приложения
    app.setStyle('Fusion')
    
    window = ClipboardManager()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
    
    
    
    
