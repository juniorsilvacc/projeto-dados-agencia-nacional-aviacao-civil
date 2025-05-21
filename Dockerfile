FROM python:3.12

WORKDIR /app

# Instalar dependências básicas para build
RUN apt-get update && apt-get install -y curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copiar apenas os arquivos de dependências para cache
COPY pyproject.toml poetry.lock* /app/

# Instalar dependências com Poetry sem criar virtualenv
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copiar o restante do código
COPY . /app/

# Comando padrão para rodar o pipeline
CMD ["python", "main.py"]
