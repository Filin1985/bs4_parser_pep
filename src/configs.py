import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import (
    LOG_FORMAT,
    DT_FORMAT,
    LOG_DIR,
    LOG_FILE,
    PRETTY_FORMAT,
    FILE_FORMAT
)


def configure_argument_parser(available_modes):
    """Добавление аргументов командной строки."""
    parser = argparse.ArgumentParser(description='Парсер документации Python')
    parser.add_argument(
        'mode',
        choices=available_modes,
        help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=(PRETTY_FORMAT, FILE_FORMAT),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging():
    """Настройки логирования."""
    LOG_DIR.mkdir(exist_ok=True)
    rotating_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
