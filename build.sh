#!/usr/bin/env bash

# Скачиваем и устанавливаем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Устанавливаем зависимости, собираем статику и применяем миграции
make install && make collectstatic && make migrate