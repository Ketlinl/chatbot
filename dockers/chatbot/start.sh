#!/bin/bash
echo "Criando as migrações no banco de dados"
python3 manage.py makemigrations
python3 manage.py migrate

echo "Rodando o servidor"
gunicorn --bind 0.0.0.0:8000 config.wsgi --reload --graceful-timeout=300 --timeout=300 --workers 3
