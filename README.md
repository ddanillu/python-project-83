# Page Analyzer

Веб-приложение для анализа веб-страниц. Позволяет добавлять URL-адреса, проверять их доступность и извлекать метаданные (заголовок, описание, H1).

### Hexlet tests and linter status:
[![Actions Status](https://github.com/ddanillu/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ddanillu/python-project-83/actions)

### Quality Status
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=ddanillu_python-project-83&metric=coverage)](https://sonarcloud.io/summary/new_code?id=ddanillu_python-project-83)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=ddanillu_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=ddanillu_python-project-83)
[![Build](https://github.com/ddanillu/python-project-83/actions/workflows/build.yml/badge.svg)](https://github.com/ddanillu/python-project-83/actions/workflows/build.yml)

### Available Application
You can see the results at the following address:
[Link to the application](https://python-project-83-97a4.onrender.com)

## Описание

Page Analyzer — это Flask-приложение для мониторинга и анализа веб-страниц. Приложение позволяет:

- Добавлять URL-адреса для анализа
- Проверять доступность страниц
- Извлекать метаданные: HTTP статус-код, заголовок H1, тег `<title>`, мета-описание
- Просматривать историю проверок для каждого URL
- Автоматически очищать старые записи (старше 1 дня)

## Технологии

- **Python 3.12+**
- **Flask** — веб-фреймворк
- **PostgreSQL** — база данных
- **BeautifulSoup4** — парсинг HTML
- **Requests** — HTTP-запросы
- **Gunicorn** — WSGI-сервер для production
- **Ruff** — линтер и форматтер кода
- **UV** — менеджер пакетов

## Установка и запуск

### Требования

- Python 3.12.3 или выше
- PostgreSQL
- UV (менеджер пакетов)

### Установка зависимостей

```bash
make install
```

Или вручную:

```bash
uv sync
```

### Настройка базы данных

1. Создайте базу данных PostgreSQL
2. Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
```

3. Инициализируйте схему базы данных:

```bash
psql -a -d $DATABASE_URL -f db/database.sql
```

Или используйте скрипт сборки:

```bash
./build.sh
```

### Запуск в режиме разработки

```bash
make dev
```

Приложение будет доступно по адресу: `http://localhost:5778`

### Запуск в production режиме

```bash
make start
```

Или с указанием порта:

```bash
PORT=8989 make start
```

## Использование

1. **Добавление URL**: Введите URL в форму на главной странице
2. **Просмотр списка**: Перейдите на страницу `/urls` для просмотра всех добавленных URL
3. **Проверка URL**: На странице конкретного URL нажмите кнопку "Проверить" для выполнения анализа
4. **Просмотр истории**: На странице URL отображается история всех проверок с метаданными

## Структура проекта

```
python-project-83/
├── page_analyzer/          # Основной пакет приложения
│   ├── __init__.py
│   ├── app.py              # Flask-приложение и маршруты
│   ├── db_manager.py       # Работа с базой данных
│   ├── checker.py          # Проверка URL и извлечение метаданных
│   ├── validator.py        # Валидация URL
│   └── templates/          # HTML-шаблоны
│       ├── index.html
│       ├── list_urls.html
│       ├── show_url.html
│       └── ...
├── db/
│   └── database.sql        # SQL-схема базы данных
├── pyproject.toml          # Конфигурация проекта и зависимости
├── Makefile                # Команды для разработки
├── build.sh                # Скрипт сборки
└── README.md
```

## API Endpoints

- `GET /` — главная страница с формой добавления URL
- `POST /urls` — добавление нового URL
- `GET /urls` — список всех URL
- `GET /urls/<id>` — страница конкретного URL с историей проверок
- `POST /urls/<id>/checks` — выполнение проверки URL

## Линтинг

Запуск линтера:

```bash
make lint
```

## Сборка

Сборка проекта:

```bash
make build
```

## Особенности

- Валидация URL перед добавлением
- Проверка на дубликаты URL
- Автоматическая очистка старых записей (старше 1 дня)
- Обработка ошибок при проверке недоступных URL
- Пул соединений с базой данных для оптимизации производительности

## Лицензия

Проект создан в рамках обучения на Hexlet.
