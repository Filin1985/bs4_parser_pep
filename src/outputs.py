import csv
import datetime as dt
import logging
from prettytable import PrettyTable

from constants import DATETIME_FORMAT, BASE_DIR


SAVE_MESSAGE = (
    'Файл с результатами был сохранён: {file_path}'
)


def control_output(results, cli_args):
    outputs = {
        'pretty': pretty_output,
        'file': file_output,
        '': default_output
    }
    output = cli_args.output
    if not output:
        output = ''
    outputs[output](results, cli_args)


def default_output(results, cli_args):
    for row in results:
        print(*row)


def pretty_output(results, cli_args):
    print(results)
    try:
        table = PrettyTable()
        table.field_names = results[0]
        table.align = 'l'
        table.add_rows(results[1:])
        print(table)
    except Exception as e:
        print(e)


def file_output(results, cli_args):
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    print(file_path)
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect=csv.unix_dialect)
        writer.writerows(results)
    logging.info(SAVE_MESSAGE.format(file_path=file_path))
