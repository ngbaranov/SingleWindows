# Используем официальный образ Python
FROM python:3.12.7

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY ./app /app

# Копируем файл requirements.txt и устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем файл config.py и alembic.ini
COPY config.py /app/config.py
COPY alembic.ini /app/alembic.ini

# Копируем файл .env
COPY .env /app/.env

# Открываем порт для приложения
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]