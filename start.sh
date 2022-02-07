#!/bin/bash
echo "Criando as migrações no banco de dados"
python3 manage.py makemigrations
python3 manage.py migrate

echo "Rodando o servidor"
python3 manage.py runserver
