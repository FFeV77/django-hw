# CRUD


Сервер проекта включает в себя 3 образа:
  - pythonapp: сервер python с исходным кодом проекта на Django + Gunicorn
  - db: стандартный сервер postgres
  - nginx: стандартный сервер nginx для проксирования и обработки статических файлов.
  
  
Для запуска проекта необходимо:

1. Собрать статику:
  python manage.py collectstatic
  
2. Отредактировать переменные окружения

3. Запустить оркестрацию
  docker compose up -d --build
  
4. После запуска сервера postgres, выполнить миграции
  python manage.py migrate
