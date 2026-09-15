import glob
import os
import sys

from core_ai import VanguardAI  # Переносим ИИ под управление Шелла
from executor import VanguardExecutor  # Импортируем наш созданный запуск процессов


class VanguardShell:
    def __init__(self):
        # Подключаем наш исполнитель скриптов
        self.executor = VanguardExecutor()
        self.ai_core = VanguardAI()

    def handle_command(self, query):
        """Единая точка обработки ВСЕХ команд и запросов Vanguard OS"""
        cmd = query.strip().lower()

        # 1. КОМАНДА ВЫХОДА ИЗ ОС (/exit или /shutdown)
        if cmd in ["/exit", "/shutdown", "выход"]:
            # Возвращаем специальный флаг завершения работы
            return ">> SHUTTING DOWN VANGUARD ENVIRONMENT...", "SYSTEM_EXIT"

        # 2. КОМАНДА ОЧИСТКИ ПАПКИ (/wipe)
        elif cmd == "/wipe":
            log = ">> INITIATING STORAGE PURGE PROTOCOL...\n"
            generated_files = glob.glob("vanguard_gen_*.py")
            deleted_count = 0
            for file_path in generated_files:
                try:
                    os.remove(file_path)
                    log += f">> PURGED: {file_path}\n"
                    deleted_count += 1
                except Exception as ex:
                    log += f">> ERROR DELETING {file_path}: {ex}\n"
            log += f"\n>> PURGE COMPLETE. TOTAL FILES DESTROYED: {deleted_count}\n"
            return log, "DISPLAY_OUTPUT"


        # 3. КОМАНДА ПОЛНОГО СБРОСА ЭКРАНА (/reset)
        elif cmd == "/reset":
            # [ДОБАВИТЬ ЭТУ СТРОКУ] Намертво вычищаем контекст из нейросети
            self.ai_core.clear_memory()

            log = (
                "==================================================\n"
                "                VANGUARD SYSTEM RESET             \n"
                "==================================================\n"
                ">> WIPING DISPLAY BUFFER...\n"
                ">> DISCONNECTING PREVIOUS NEURAL CONTEXT... DONE\n"
                ">> VANGUARD KERNEL: READY FOR NEW INSTRUCTIONS.\n"
            )
            return log, "DISPLAY_OUTPUT"

        # 4. КОМАНДА АСИНХРОННОГО ЗАПУСКА СКРИПТОВ (/run <id>)
        elif cmd.startswith("/run"):
            parts = query.split()
            if len(parts) < 2:
                return (
                    ">> ERROR: Specify file ID. Example: /run 553\n",
                    "DISPLAY_OUTPUT",
                )

            file_id = parts

            def async_execute():
                execution_log = self.executor.execute_script(file_id)
                print(f"\n{execution_log}\n")

            import threading

            threading.Thread(target=async_execute, daemon=True).start()
            return (
                f">> INITIATING PROCESS FOR VANGUARD_GEN_{file_id}.PY...\n>> STREAMING OUTPUT TO PYCHARM CONSOLE.\n",
                "DISPLAY_OUTPUT",
            )
            # [NEW] КОМАНДА: ВЫВОД СПИСКА СГЕНЕРИРОВАННЫХ СКРИПТОВ (/apps)
        elif cmd == "/apps":
            generated_files = glob.glob("vanguard_gen_*.py")
            if not generated_files:
                return (
                    ">> VANGUARD REGISTRY: No generated applications found.\n",
                    "DISPLAY_OUTPUT",
                )

            log = (
                "==================================================\n"
                "             VANGUARD APPLICATION REGISTRY        \n"
                "==================================================\n"
            )
            for file_path in generated_files:
                # Получаем размер файла в КБ
                file_size = os.path.getsize(file_path) / 1024
                log += f"-> [ID: {file_path[13:-3]}] | FILE: {file_path} | SIZE: {file_size:.2f} KB\n"
            log += (
                "==================================================\n"
                ">> TYPE: /run <id> to execute targeted script.\n"
            )
            return log, "DISPLAY_OUTPUT"
            # [NEW] КОМАНДА: ДЕТАЛЬНЫЙ АУДИТ ЖЕЛЕЗА ПК (/hardware)
        elif cmd == "/hardware":
            import psutil

            # Сбор информации о памяти и ядрах
            cores_physical = psutil.cpu_count(logical=False)
            cores_logical = psutil.cpu_count(logical=True)
            ram = psutil.virtual_memory()

            log = (
                "==================================================\n"
                "               VANGUARD HARDWARE AUDIT            \n"
                "==================================================\n"
                ">> ARCHITECTURE: AMD64/x86_64 SECURED ENVIRONMENT\n"
                f">> CPU INFRASTRUCTURE: {cores_physical} Physical Cores | {cores_logical} Threads\n"
                f">> SYSTEM RAM CAPACITY: {ram.total / (1024**3):.2f} GB Total\n"
                f">> RAM CURRENTLY AVAILABLE: {ram.available / (1024**3):.2f} GB Free\n"
                f">> PLATFORM INTEGRITY: 100% SUVEREIGN KERNEL\n"
                "==================================================\n"
            )
            return log, "DISPLAY_OUTPUT"
            # [NEW] КОМАНДА: ВЫВОД РУКОВОДСТВА ПО СИСТЕМЕ (/help)
        elif cmd == "/help":
            log = (
                "==================================================\n"
                "               VANGUARD SHELL COMMANDS            \n"
                "==================================================\n"
                ">> /help     -> Display this tactical instruction log.\n"
                ">> /apps     -> List all AI auto-compiled python applications.\n"
                ">> /run <id> -> Execute targeted python script in background thread.\n"
                ">> /hardware -> Perform deep hardware audit and scan resources.\n"
                ">> /wipe     -> Purge and destroy all compiled vanguard scripts.\n"
                ">> /reset    -> Clear display buffer and reset neural channel.\n"
                ">> /exit     -> Soft shutdown of the Vanguard OS infrastructure.\n"
                "==================================================\n"
            )
            return log, "DISPLAY_OUTPUT"

        # 5. ЕСЛИ ЭТО ОБЫЧНЫЙ ЗАПРОС К ИИ — ПЕРЕДАЕМ УПРАВЛЕНИЕ СТРИМЕРУ
        else:
            # Возвращаем пустую строку и флаг, разрешающий потоковый ИИ
            return "", "AI_STREAM_ALLOWED"
