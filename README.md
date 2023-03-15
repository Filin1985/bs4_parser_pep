# Проект парсинга pep документации

## Описание проекта

Программа парсит сайты https://docs.python.org/3/ и https://peps.python.org/ и выдает информацию о последних изменениях в PEP и статистику по статусам всех PEP

**Используемые технологии**

- BeautifulSoup

### Запуск проекта

1. Клонируем репозиторий

```
git clone https://github.com/Filin1985/bs4_parser_pep.git
```

2. Устанавливаем виртуальное окружение

```
python3 -m venv venv
```

3. Активируем виртуальное окружение

```
source venv/bin/activate
```

4. Устанавливаем зависимости

```
pip install -r requirements.txt
```

5. Заходим в папку src

```
cd src
```

### Запуск парсеров

<details>
  <summary>whats-new</summary>
  <p>Выводит данные по изменениям в языке Python</p>
  ```
    python main.py whats-new [параметры]
  ```
</details>
