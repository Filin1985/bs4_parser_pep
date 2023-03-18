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
    """Отправка запроса и обработка ошибки RequestException."""
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException:
        raise ConnectionError(ERROR_MESSAGE.format(url=url))


def find_tag(soup, tag, attrs=None):
    """Поиск тега и перехват ошибки отсутствия тега."""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        raise ParserFindTagException(
            TAG_MESSAGE.format(tag=tag, attrs=attrs)
        )
    return searched_tag


def create_soup(session, url, features='lxml'):
    """Отправка запроса и создание объекта BeautifulSoup."""
    return BeautifulSoup(get_response(session, url).text, features)
