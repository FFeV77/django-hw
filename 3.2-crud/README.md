# CRUD


Сервер проекта включает в себя 3 контейнера:
  - pythonapp: сервер python с исходным кодом проекта на Django + Gunicorn
  - db: стандартный сервер postgres
  - nginx: стандартный сервер nginx для проксирования и обработки статических файлов.
  
  
Для запуска проекта необходимо:
  
1. Отредактировать переменные окружения

2. Запустить оркестрацию
  ```
  docker compose -f Docker-compose.yml up -d --build
  ```
  
3. После запуска сервера postgres, выполнить миграции
  ```
  docker compose -f Docker-compose.yml exec pythonapp python manage.py migrate --noinput
  ```
