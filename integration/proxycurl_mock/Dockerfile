FROM python:3.12-slim
EXPOSE 5000

WORKDIR /app

COPY ./app.py /app
COPY ./data/ /app

RUN pip install --no-cache-dir Flask


CMD ["python", "app.py"]
