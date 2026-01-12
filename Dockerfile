# Use a imagem oficial do Python 3.11 como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Define variáveis de ambiente para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta 5000 (porta padrão da API)
EXPOSE 5000

# Define a variável de ambiente para produção
ENV FLASK_ENV=production
ENV DEBUG=False
ENV API_HOST=0.0.0.0
ENV API_PORT=5000

# Instala gunicorn para production
RUN pip install gunicorn

# Comando para iniciar a aplicação com gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]
