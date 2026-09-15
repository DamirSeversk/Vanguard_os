import os
import sys

# Автоматический адаптер путей для PyInstaller (Фикс ошибки frozen/import)
if getattr(sys, "frozen", False):
    # Если это скомпилированный .exe, принудительно переключаем рабочую директорию
    # на временную папку, куда распаковались ваши скрипты (shell.py, gui.py)
    current_dir = sys._MEIPASS
    os.chdir(current_dir)
    sys.path.insert(0, current_dir)
else:
    # Если запускаем обычный скрипт в PyCharm
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)

import tkinter as tk

from gui_desktop import VanguardOS

if __name__ == "__main__":
    # Создаем главное графическое окно Windows
    root = tk.Tk()

    # Инициализируем нашу разделенную операционную систему
    app = VanguardOS(root)

    # Запускаем бесконечный цикл обработки событий интерфейса
    root.mainloop()
