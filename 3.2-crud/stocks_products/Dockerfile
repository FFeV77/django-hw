FROM python:3-slim
# RUN apt-get update && \
# addgroup --system test && adduser --system --addgroup test
# USER test

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /usr/src/app
COPY . .

EXPOSE 8000
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "stocks_products.wsgi:application"]
HEALTHCHECK CMD curl --fail http://localhost:8000 || exit 1