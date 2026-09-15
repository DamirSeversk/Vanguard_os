import pytest

from shell import VanguardShell


@pytest.fixture
def active_shell():
    """Фикстура для автоматического создания чистого экземпляра шелла перед каждым тестом"""
    return VanguardShell()


def test_shell_help_command(active_shell):
    """Тестируем, что команда /help возвращает мануал и правильное действие DISPLAY_OUTPUT"""
    log, action = active_shell.handle_command("/help")

    assert action == "DISPLAY_OUTPUT"
    assert "VANGUARD SHELL COMMANDS" in log
    assert "/hardware" in log


def test_shell_hardware_command(active_shell):
    """Тестируем, что аудит железа /hardware возвращает информацию о системе"""
    log, action = active_shell.handle_command("/hardware")

    assert action == "DISPLAY_OUTPUT"
    assert "HARDWARE AUDIT" in log
    assert "GB Total" in log


def test_shell_reset_command(active_shell):
    """Тестируем сброс экрана /reset и очистку контекста ИИ"""
    log, action = active_shell.handle_command("/reset")

    assert action == "DISPLAY_OUTPUT"
    assert "SYSTEM RESET" in log
    assert "READY FOR NEW INSTRUCTIONS" in log


def test_shell_exit_command(active_shell):
    """Тестируем, что команда выхода возвращает флаг SYSTEM_EXIT"""
    log, action = active_shell.handle_command("/exit")

    assert action == "SYSTEM_EXIT"
    assert "SHUTTING DOWN" in log


def test_shell_run_without_id(active_shell):
    """Тестируем обработку ошибки, если написать /run без указания ID файла"""
    log, action = active_shell.handle_command("/run")

    assert action == "DISPLAY_OUTPUT"
    assert "ERROR: Specify file ID" in log


def test_shell_ai_fallback(active_shell):
    """Тестируем, что любой обычный текст отправляет нас в стример ИИ"""
    log, action = active_shell.handle_command("Привет, напиши код для сортировки")

    assert action == "AI_STREAM_ALLOWED"
    assert log == ""
