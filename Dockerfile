# Базовий образ Python
FROM python:3.12-slim

# Робоча директорія
WORKDIR /app

# Встановлюємо системні пакети для mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо файли проєкту
COPY . /app

# Встановлюємо залежності Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Порт для Flask
EXPOSE 5000

# Команда запуску сервісу
CMD ["python", "app.py"]
