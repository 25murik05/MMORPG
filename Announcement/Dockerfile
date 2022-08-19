FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python manage.py migrate

RUN python manage.py makemigrations

