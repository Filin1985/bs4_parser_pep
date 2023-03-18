# Проект парсинга документации Python

## Описание проекта

Программа парсит сайты https://docs.python.org/3/ и https://peps.python.org/ и выдает информацию о последних изменениях в PEP и статистику по статусам всех PEP

**Используемые технологии**

- Python
- BeautifulSoup
- PrettyTable

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
  <summary>Режим "whats-new"</summary>
  <p>Выводит данные по изменениям в языке Python</p>
  <code>python main.py whats-new [параметры]</code>
</details>

<details>
  <summary>Режим "latest-versions"</summary>
  <p>Выводит список версий Python</p>
  <code>python main.py latest-versions [параметры]</code>
</details>

<details>
  <summary>Режим "pep"</summary>
  <p>Выводит данные по изменениям в языке Python</p>
  <code>python main.py pep [параметры]</code>
</details>

<details>
  <summary>Режим "download"</summary>
  <p>Скачивает документацию Python в zip архиве в папку downloads</p>
  <code>python main.py download [параметры]</code>
</details>

### Варианты параметров

<details>
  <summary>Режим "-h" или "--help"</summary>
  <p>Выводит справочную информацию о возможных командах парсера</p>
  <code>python main.py -h</code>
</details>

<details>
  <summary>Режим "-с" или "--clear-cache"</summary>
  <p>Очищает кэш</p>
  <code>python main.py latest-versions -с</code>
</details>

<details>
  <summary>Режим "-o" или "--output"</summary>
  <p>Задает способы выводы данных. Возможны следующие варианты:</p>
  <p>1. pretty - выводит данные в виде таблице</p>
  <p>2. file - сохраняет файл в формате .csv в папку results/</p>
  <code>python main.py pep -o file</code>
</details>

**Авторы: [ЯндексПрактикум]('https://github.com/yandex-praktikum), [Марат Ихсанов]('https://github.com/Filin1985)**
