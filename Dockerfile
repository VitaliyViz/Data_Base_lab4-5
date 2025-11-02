# Базовий образ Python
FROM python:3.12-slim

# Встановлюємо змінну для неінтерактивної установки пакунків
ENV DEBIAN_FRONTEND=noninteractive

# Робоча директорія
WORKDIR /app

# Встановлюємо системні пакети для mysqlclient та очищаємо кеш apt одразу
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо тільки requirements спершу (кешування Docker)
COPY requirements.txt .

# Оновлюємо pip і встановлюємо Python-залежності без кешу
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копіюємо решту файлів проєкту
COPY . /app

# Порт для Flask
EXPOSE 5000

# Команда запуску сервісу
CMD ["python", "app.py"]
