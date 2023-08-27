import logging
import os


def setup_logging():
    # для винды
    # log_path = r"C:\logs"
    # для мак
    log_path = "logs"

    # Создание папки, если она не существует
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # Создание объекта логгера
    logger = logging.getLogger("my_app_logger")

    # Установка уровня логирования (например, DEBUG, INFO, WARNING, ERROR)
    logger.setLevel(logging.DEBUG)

    # Создание обработчика для записи в файл
    log_file = os.path.join(log_path, "app.log")
    file_handler = logging.FileHandler(log_file, mode='a')

    # Установка уровня логирования для обработчика
    file_handler.setLevel(logging.DEBUG)

    # Создание форматтера для задания формата записи сообщений лога
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Установка форматтера для обработчика
    file_handler.setFormatter(formatter)

    # Добавление обработчика в логгер
    logger.addHandler(file_handler)

    return logger


# Вызов функции для настройки логирования
logger = setup_logging()
