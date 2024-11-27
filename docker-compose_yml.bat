services:
  web:
    build:
      context: .
      dockerfile: ./app/Dockerfile
    command: uvicorn app.main:app --host 0.0.0.0
    ports:
      - '8000:8000'