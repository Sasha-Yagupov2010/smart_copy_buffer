import keyboard
import pyperclip
import time

# список для хранения истории
clipboard_history = []

# функция, которая вызывается при нажатии Ctrl+C
def on_copy():
    # получаем текущий текст из буфера обмена
    text = pyperclip.paste()
    clipboard_history.append(text)

    print(f"Скопировано: {text}")

# устанавливаем глобальный перехват Ctrl+C
keyboard.add_hotkey('ctrl+c', on_copy)

print("Программа запущена. Нажмите Ctrl+C для копирования текста в историю.")
print("Чтобы завершить, нажмите ESC.")


def send():
    text_to_copy = ""
    for i in clipboard_history:
        text_to_copy += '\n'+i
    
    print(text_to_copy)    
    pyperclip.copy(text_to_copy)    


keyboard.add_hotkey('ctrl+1', send)


try:
    keyboard.wait('esc')
except KeyboardInterrupt:
    pass



    


