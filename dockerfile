# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

RUN mkdir logs
RUN touch /app/logs/logs.log
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD ["python3", "./main/application.py"]