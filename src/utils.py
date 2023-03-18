from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException

ERROR_MESSAGE = (
    'Ошибка при загрузке страницы по адресу {url}'
)

TAG_MESSAGE = (
    'Не найден тег {tag} {attrs}'
)


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException:
        raise ConnectionError(ERROR_MESSAGE.format(url=url))


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error = TAG_MESSAGE.format(tag=tag, attrs=attrs)
        raise ParserFindTagException(error)
    return searched_tag


def create_soup(session, url_address):
    response = get_response(session, url_address)
    if response is None:
        return
    return BeautifulSoup(response.text, features="lxml")
