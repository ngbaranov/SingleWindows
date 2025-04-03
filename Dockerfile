# Используем официальный образ Python
FROM python:3.12.7

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем файлы приложения в контейнер
COPY ./app /code/app
COPY ./alembic.ini /code/alembic.ini
COPY ./config.py /code/config.py
COPY ./.env /code/.env
COPY ./requirements.txt /code/requirements.txt
COPY ./main.py /code/main.py
COPY ./auth /code/auth
COPY ./admin_panel /code/admin_panel

# Копируем файл requirements.txt и устанавливаем зависимости
RUN pip install --no-cache-dir -r /code/requirements.txt




# Создаем директорию для загрузки файлов и устанавливаем права
RUN mkdir -p /code/app/static/files && chmod -R 777 /code/app/static/files


# Открываем порт для приложения
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]