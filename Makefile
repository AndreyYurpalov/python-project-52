build:
	./build.sh

install:
	uv pip install -r requirements.txt

# Собираем статику
collectstatic:
	python3 manage.py collectstatic --noinput

# Применяем миграции
migrate:
	python3 manage.py migrate

render-start:
	gunicorn task_manager.wsgi
