## Stage 01: Pegar os arquivos estáticos ##
###########################################

# Pega a imagem do python3.8 e armazena na
# variavel builder temporariamente
FROM python:3.8 as builder

# Instala as dependencias do sistema operacional
RUN apt-get update && pip3 install --upgrade pip

# Instala os pacotes do projeto
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copia o código para a pasta software do container
ADD . /software
WORKDIR /software

# Retorna os arquivos estáticos do projeto.
RUN python3 manage.py collectstatic --noinput

##################################################################
## Stage 02: Configurando o servidor para os arquivos estaticos ##
##################################################################

# Pega a imagem do nginx
FROM nginx:latest

# Remove os arquivos defaults do nginx
RUN rm -rf /etc/nginx/conf.d/*

# Copia o arquivo de configuração do nginx para dentro do container
COPY ./dockers/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Remove a página default do nginx
RUN rm -rf /usr/share/nginx/html/*

# Pega os arquivos estaticos gerados na etapa 01 e insere no servidor
COPY --from=builder /software/config/staticfiles /usr/share/nginx/html

# Expoem a porta 80
EXPOSE 80

# Roda o servidor nginx
CMD ["nginx", "-g", "daemon off;"]
