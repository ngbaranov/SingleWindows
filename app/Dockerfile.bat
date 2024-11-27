FROM python:3.12.7
# устанавливаем переменные окружения
ENV HOME=/home/single_windows  \
    APP_HOME=/home/single_windows\
    PYTHONPATH="${PYTHONPATH}:/home/single_windows" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# создаем домашнюю директорию для пользователя(/home/fast) и директорию для проекта(/home/fast/app)
# создаем группу fast
# создаем отдельного пользователя fast
RUN mkdir -p $APP_HOME \
    && groupadd -r sw \
    && useradd -r -g sw sw

# устанавливаем рабочую директорию
WORKDIR $HOME

# копирование проекта FastAPI в рабочую директорию
COPY app app
ADD alembic.ini .


# обновление pip
# установка зависимостей из списка requirements.txt
# изменение владельца, для всех директорий и файлов проекта, на пользователя fast
RUN pip install --upgrade pip \
    && pip install -r app/requirements.txt \
    && chown -R sw:sw .

# изменение рабочего пользователя на sw
USER sw

