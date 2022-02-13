# Nome do arquivo: Makefile
# Propósito  	 : Simplifica e agiliza o desenvolvimento

# DATABASE -----------------------------------------------------

migrations:
	# Cria todas as migrações
	docker-compose exec chatbot python3 manage.py makemigrations

migrate:
	# Rodas as migrações no banco de dados
	docker-compose exec chatbot python3 manage.py migrate

shell:
	# Roda o shell do django
	docker-compose exec chatbot python3 manage.py shell

dbshell:
	# Entrar no database do banco de dados
	docker-compose exec chatbot python3 manage.py dbshell

superuser:
	# Cria um superusuário
	docker-compose exec chatbot python3 manage.py createsuperuser

revert:
	# Reverte a migração do banco para uma especifica.
	docker-compose exec chatbot python3 manage.py migrate ${app} ${migration}

show_migrations:
	# Mostrar todas as migrações de um app.
	docker-compose exec chatbot python3 manage.py showmigrations ${app}

fix_migrations:
	# Arrumar migrações
	docker-compose exec chatbot python3 manage.py makemigrations --merge

# PACOTES ------------------------------------------------------

install:
	# Instala uma nova dependência
	docker-compose exec chatbot pip3 install ${package}

remove:
	# Remove um pacote
	docker-compose exec chatbot pip3 uninstall ${package}

requirements:
	# Verifica todas as dependências
	docker-compose exec chatbot pip3 freeze

# QUALIDADE ----------------------------------------------------

path := .

flake8:
	# Roda o flake8
	docker-compose exec chatbot_test flake8 ./projects --count

# DOCKER ---------------------------------------------------------

container := chatbot

bash:
	# Entra no terminal do container
	docker-compose exec ${container} bash

logs:
	# Visualiza os logs
	docker-compose logs -f -t ${container}

prod:
	# Sobe a aplicação em produção
	docker-compose -f docker-compose.prod.yml up


# OUTROS --------------------------------------------------

staticfiles:
	# Pega os arquivos estáticos
	docker-compose exec chatbot python3 manage.py collectstatic --noinput
