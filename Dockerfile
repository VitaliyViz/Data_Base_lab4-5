FROM python:3.12-slim

WORKDIR /app

# Встановлюємо системні пакети для збірки mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо requirements
COPY requirements.txt /app/

# Встановлюємо Python-залежності
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код
COPY . /app

# Запускаємо Gunicorn для продакшн
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1
