FROM python:3.12-slim

# Робоча директорія всередині контейнера
WORKDIR /app

# Скопіювати requirements
COPY requirements.txt /app/

# Встановити залежності
RUN pip install --no-cache-dir -r requirements.txt

# Скопіювати увесь код у контейнер
COPY . /app

# Запускаємо gunicorn
CMD ["python", "app.py"]
