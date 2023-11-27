# Usar uma imagem base do Python
FROM python:3.8-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos de requisitos primeiro para aproveitar o cache das camadas do Docker
COPY requirements.txt requirements.txt

# Instalar as dependências da aplicação
RUN pip install -r requirements.txt

# Copiar o restante dos arquivos da aplicação para o diretório de trabalho
COPY . /app

# Informar a porta que o contêiner deve expor
EXPOSE 5000

# Comando para executar a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]
