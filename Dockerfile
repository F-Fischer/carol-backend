FROM python:3.8.13-buster

COPY data /data
COPY services /services
COPY utils /utils
COPY requirements.txt /requirements.txt
COPY carol-service.py /carol-service.py

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD uvicorn carol-service:app --host 0.0.0.0 --port $PORT
