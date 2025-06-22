# Base image
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copiando o conteúdo da pasta sport para o container
COPY . .

# Instalando as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando que a aplicação vai executar
CMD ["python", "sportsmonks_project.py"]
