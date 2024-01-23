# 이미지 지정
FROM python:3.11-slim

# 환경변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# poetry 및 packages 설치
RUN mkdir /app/
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# source 복사
COPY ./src src/

# container 명령
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
