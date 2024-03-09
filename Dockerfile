FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY nginx/nginx.conf /etc/nginx/conf.d/

COPY . /app/

RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput
