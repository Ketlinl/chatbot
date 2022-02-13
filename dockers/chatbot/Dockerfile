# Instala um container com o python 3.8
FROM python:3.8
# Arrumar o delay dos logs do django e colocar o ambiente de PROD
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT production
# Instala dependencias do sistema operacional
RUN apt-get update && apt-get install -y vim && pip3 install --upgrade pip
# Cria a pasta software no container
RUN mkdir /software
# Utiliza a pasta software como a pasta principal
WORKDIR /software
# Copia o arquivo com os pacotes para dentro da pasta software
COPY ./requirements.txt /software
# Instala todos os pacotes do projeto
RUN pip3 install -r requirements.txt
# Copia o restante do código para a pasta software
COPY . /software
# Expoe a porta 8000 para o mundo externo
EXPOSE 8000
# Da permissão de execução no script start.sh
RUN chmod +x ./dockers/chatbot/start.sh
# Executa o script start.sh
ENTRYPOINT ["./dockers/chatbot/start.sh"]
