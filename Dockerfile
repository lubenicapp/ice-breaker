FROM python:3.12
ENTRYPOINT ["sh", "entrypoint.sh"]

WORKDIR /app

COPY . /app

RUN pip install pipenv
RUN pipenv install --system --dev
