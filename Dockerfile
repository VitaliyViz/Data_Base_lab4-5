# Вибираємо базовий образ Python
FROM python:3.12-slim

# Створюємо робочу директорію
WORKDIR /app

# Копіюємо файли проєкту
COPY . /app

# Встановлюємо залежності
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Експортуємо порт
EXPOSE 5000

# Команда запуску
CMD ["python", "app.py"]
