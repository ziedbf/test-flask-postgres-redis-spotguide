FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=manage.py

CMD flask run --host 0.0.0.0
