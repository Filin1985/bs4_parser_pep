from collections import defaultdict
import logging
import re
import requests_cache
from tqdm import tqdm
from urllib.parse import urljoin

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR,
    MAIN_DOC_URL,
    PEPS_URl,
    EXPECTED_STATUS,
    DOWNLOADS_DIR,
)
from outputs import control_output
from utils import find_tag, create_soup

DOWNLOAD_MESSAGE = (
    'Архив был загружен и сохранён: {archive_path}'
)

ARGS_MESSAGE = (
    'Аргументы командной строки: {args}'
)
START_MESSAGE = 'Парсер запущен!'
FINISH_MESSAGE = 'Парсер завершил работу.'
MESSAGE_ERROR = 'Ошибка при выполнении: {error}'
STATUS_MESSAGE = (
    '\n'
    'Несовпадающие статусы:\n'
    '{link}\n'
    'Статус в карточке: {pep_status}\n'
    'Ожидаемые статусы: '
    '{table_status}\n'
)
CONNECTION_ERROR = 'Сбой в работе программы: {error}'
NOT_FIND_MESSAGE = 'Ничего не нашлось в {ul}'
SOUP_ERROR = "Ссылка {link} не существует"


def whats_new(session):
    """Парсер о новинках в языке Python."""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    sections_by_python = soup.select( 
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1 a' 
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        href = section['href']
        version_link = urljoin(whats_new_url, href)
        try:
            soup = create_soup(session, version_link)
            results.append(
                (version_link,
                 find_tag(soup, 'h1').text,
                 find_tag(soup, 'dl').text.replace('\n', ' '))
            )
        except ConnectionError as error:
            logging.error(CONNECTION_ERROR.format(error=error))
    return results


def latest_versions(session):
    """Парсер последних версий Python."""
    soup = create_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
        else:
            raise KeyError(NOT_FIND_MESSAGE.format(ul=ul))
    result = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, str(a_tag))
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        result.append(
            (a_tag['href'], version, status)
        )
    return result


def download(session):
    """Парсер отвечающий за скачивание архива документации Python."""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = create_soup(session, downloads_url)
    pdf_a4_tag = soup.select_one('table.docutils a[href$="pdf-a4.zip"]')
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DOWNLOADS_DIR
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(DOWNLOAD_MESSAGE.format(archive_path=archive_path))


def pep(session):
    """Парсинг PEP документации и подсчета статусов."""
    soup = create_soup(session, PEPS_URl)
    main_tag = find_tag(soup, 'section', {'id': 'numerical-index'})
    table_row_tags = main_tag.find_all('tr')
    status_counts = defaultdict(int)
    messages = []
    for tag in tqdm(table_row_tags[1:]):
        link_href = find_tag(tag, 'a')['href']
        link = urljoin(PEPS_URl, link_href)
        try:
            soup = create_soup(session, link)
        except AttributeError:
            logging.error(SOUP_ERROR.format(link=link))
        main_pep_data = find_tag(soup, 'section', attrs={'id': 'pep-content'})
        main_pep_info = find_tag(
            main_pep_data,
            'dl',
            attrs={'class': 'rfc2822 field-list simple'}
        )
        for pep in main_pep_info:
            if not (pep.name == 'dt' and pep.text == 'Status:'):
                continue
            pep_status = pep.next_sibling.next_sibling.string
            status_counts[pep_status] += 1
            if len(tag.td.text) != 1:
                table_status = tag.td.text[1:]
                main_pep_status = tag.td.text[1:]
                if pep_status[0] != main_pep_status:
                    messages.append(
                        STATUS_MESSAGE.format(
                            link=link,
                            pep_status=pep_status,
                            table_status=EXPECTED_STATUS[table_status]
                        )
                    )
    for message in messages:
        logging.info(message)
    return [
        ('Статус', 'Количество'),
        *status_counts.items(),
        ('Всего', sum(status_counts.values())),
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'pep': pep,
    'download': download,
}


def main():
    configure_logging()
    logging.info(START_MESSAGE)
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(ARGS_MESSAGE.format(args=args))
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        results = MODE_TO_FUNCTION[args.mode](session)

        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.error(MESSAGE_ERROR.format(error=error))
    logging.info(FINISH_MESSAGE)


if __name__ == '__main__':
    main()
