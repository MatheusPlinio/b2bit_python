# Use a base image
FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN python -c "from django.core.management.utils import get_random_secret_key; \
    import os; \
    os.environ['DJANGO_SECRET_KEY'] = get_random_secret_key(); \
    print('SECRET_KEY generated and set as environment variable')"

COPY . .

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && python manage.py seed && python manage.py collectstatic --noinput && gunicorn app.wsgi:application --bind 0.0.0.0:8000"]
