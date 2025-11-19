import keyboard
import pyperclip
import time
import os
from datetime import datetime

# Константы
MAX_HISTORY_SIZE = 100
HISTORY_FILE = "clipboard_history.txt"

# список для хранения истории (простой список строк)
clipboard_history = []

def load_history():
    """Загрузка истории из файла при старте"""
    global clipboard_history
    try:
        if os.path.exists(HISTORY_FILE):  # Проверяем существование файла
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                clipboard_history = [line.strip() for line in f.readlines()]  # Убираем символы новой строки
            print(f"Загружено {len(clipboard_history)} записей из истории")
        else:
            print("Файл истории не найден, начинаем с пустой истории")
            clipboard_history = []
    except Exception as e:
        print(f"Ошибка загрузки истории: {e}")
        clipboard_history = []

def save_history():
    """Сохранение истории в файл"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            for item in clipboard_history:
                f.write(item + '\n')  # Добавляем символ новой строки для каждого элемента
        print(f"История сохранена ({len(clipboard_history)} записей)")
    except Exception as e:
        print(f"Ошибка сохранения истории: {e}")

# функция, которая вызывается при нажатии Ctrl+C
def on_copy():
    # получаем текущий текст из буфера обмена
    text = pyperclip.paste()
    
    # Проверяем, не является ли текст дубликатом последней записи
    if clipboard_history and text == clipboard_history[-1]:
        print("Дубликат последней записи - пропускаем")
        return
    
    clipboard_history.append(text)
    
    # Ограничиваем размер истории
    if len(clipboard_history) > MAX_HISTORY_SIZE:
        clipboard_history.pop(0)
        print("История достигла максимального размера, удалена старая запись")
    
    # Автосохранение после каждого добавления!
    save_history()
    
    print(f"Скопировано: {text[:50]}{'...' if len(text) > 50 else ''}")

def send():
    """Скопировать всю историю в буфер обмена"""
    if not clipboard_history:
        print("История пуста")
        return
        
    text_to_copy = "\n".join(clipboard_history)  # Более эффективное объединение
    
    print(f"Скопировано {len(clipboard_history)} записей в буфер обмена")
    pyperclip.copy(text_to_copy)

def show_stats():
    """Показать статистику истории"""
    print(f"=== Статистика ===")
    print(f"Всего записей: {len(clipboard_history)}")
    if clipboard_history:
        print("Последние 3 записи:")
        # Берем последние 3 элемента и переворачиваем для отображения от новой к старой
        last_three = clipboard_history[-3:]
        for i, text in enumerate(reversed(last_three)):
            print(f"  {i+1}. {text[:50]}{'...' if len(text) > 50 else ''}")
    else:
        print("История пуста")

def clear_history():
    """Очистка истории"""
    global clipboard_history
    clipboard_history.clear()
    save_history()
    print("История очищена")

# Загружаем историю при старте
load_history()

# устанавливаем глобальный перехват Ctrl+C
keyboard.add_hotkey('ctrl+c', on_copy)

print("Программа запущена. Нажмите Ctrl+C для копирования текста в историю.")
print("Чтобы завершить, нажмите ESC.")

# Горячие клавиши
keyboard.add_hotkey('ctrl+1', send)
keyboard.add_hotkey('ctrl+2', show_stats)
keyboard.add_hotkey('ctrl+0', clear_history)

print("Горячие клавиши:")
print("Ctrl+C - добавить в историю")
print("Ctrl+1 - скопировать всю историю")
print("Ctrl+2 - показать статистику")
print("Ctrl+0 - очистить историю")

try:
    keyboard.wait('esc')
except KeyboardInterrupt:
    pass
finally:
    # Сохраняем историю при выходе
    save_history()
    print("История сохранена. Программа завершена.")