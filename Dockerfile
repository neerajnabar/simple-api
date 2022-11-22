FROM python:3.11-buster

WORKDIR /app

COPY ["server.py", "app.py", "views.py", "./"]

CMD ["python3","server.py","-p","8000"]
