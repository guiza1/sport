# Base image
FROM python:3.11-slim

# Instalar cron e ferramentas básicas
RUN apt-get update && apt-get install -y \
    cron \
    vim \
    nano \
    curl \
    wget \
    dnsutils \
    net-tools \
    iputils-ping \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Diretório da app
WORKDIR /app

# Copiar o conteúdo
COPY . .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt


# Variáveis de ambiente que podes definir via EasyPanel
ENV SUPABASE_URL="https://sua-url-do-supabase"
ENV SUPABASE_KEY="sua-chave-do-supabase"
ENV DB_HOST="aws-0-eu-north-1.pooler.supabase.com"
ENV DB_PORT="5432"
ENV DB_USER="seu-usuario"
ENV DB_PASSWORD="sua-senha"
ENV DB_NAME="postgres"

# Criar o log
RUN touch /app/script.log

# Rodar cron
CMD ["cron", "-f"]
