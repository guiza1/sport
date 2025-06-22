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

# Configurar cron
RUN echo "0 */6 * * * python /app/sportsmonks_project.py >> /app/script.log 2>&1" > /etc/cron.d/schedule \
    && chmod 0644 /etc/cron.d/schedule \
    && crontab /etc/cron.d/schedule

# Variáveis de ambiente que podes definir via EasyPanel
ENV SUPABASE_URL="https://sua-url-do-supabase"
ENV SUPABASE_KEY="sua-chave-do-supabase"

# Criar o log
RUN touch /app/script.log

# Rodar cron
CMD ["cron", "-f"]
