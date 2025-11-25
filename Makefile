# Команда для синхронизации окружения
install:
	uv sync

# Команда для установки пакета
package-install:
	uv tool install dist/*.whl

# Команда для запуска сервера в режиме разработки
dev:
	uv run flask --debug --app page_analyzer:app run

# Команда для линтинга с использованием ruff
lint:
	uv run ruff check

# Конфигурация порта со значением по умолчанию
PORT ?= 8000

# Команда для запуска приложения с gunicorn
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

# Команда для сборки приложения
build:
	./build.sh

# Команда для запуска приложения на render.com
render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app