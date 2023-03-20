import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (
    DATETIME_FORMAT,
    BASE_DIR,
    PRETTY_FORMAT,
    FILE_FORMAT,
    RESULTS_DIR
)


SAVE_MESSAGE = (
    'Файл с результатами был сохранён: {file_path}'
)


def default_output(results, cli_args):
    """Построчный вывод результатов в терминал."""
    for row in results:
        print(*row)


def pretty_output(results, cli_args):
    """Вывод данных в формате PrettyTable."""
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    """Создание директории results и запись данных в файл."""
    results_dir = BASE_DIR / RESULTS_DIR
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        csv.writer(
            f, dialect=csv.unix_dialect
        ).writerows(results)
    logging.info(SAVE_MESSAGE.format(file_path=file_path))


OUTPUTS = {
    PRETTY_FORMAT: pretty_output,
    FILE_FORMAT: file_output,
    None: default_output
}


def control_output(results, cli_args):
    """Вывод разных результатов парсинга."""
    OUTPUTS[cli_args.output](results, cli_args)
