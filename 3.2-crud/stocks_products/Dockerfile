FROM python:3-slim

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /project

EXPOSE 8000
WORKDIR /project
RUN python manage.py migrate && \
python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "stocks_products.wsgi:application"]