# Base image
FROM python:3.11-slim

# Instalar ferramentas básicas e dependências nativas para psycopg2
RUN apt-get update && apt-get install -y \
    vim \
    nano \
    curl \
    wget \
    dnsutils \
    net-tools \
    iputils-ping \
    gcc \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Diretório da app
WORKDIR /app

# Copiar o conteúdo da app
COPY . .

# Atualizar requirements para psycopg2-binary, caso esteja listado
RUN sed -i 's/^psycopg2$/psycopg2-binary/' requirements.txt || true

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Variáveis de ambiente que podes definir via EasyPanel
ENV SUPABASE_URL="https://sua-url-do-supabase"
ENV SUPABASE_KEY="sua-chave-do-supabase"
ENV DB_HOST="aws-0-eu-north-1.pooler.supabase.com"
ENV DB_PORT="6543"
ENV DB_USER="seu-usuario"
ENV DB_PASSWORD="sua-senha"
ENV DB_NAME="postgres"

# Manter o container ativo esperando comandos
CMD ["tail", "-f", "/dev/null"]
