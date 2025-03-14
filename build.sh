#!/usr/bin/env bash

# Скачиваем и устанавливаем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

source $HOME/.local/bin/env

# Устанавливаем зависимости
uv pip install -r requirements.txt

# Собираем статику
python manage.py collectstatic --noinput

# Применяем миграции
python manage.py migrate



# Устанавливаем зависимости, собираем статику и применяем миграции
# make install && make collectstatic && make migrate