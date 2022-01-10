FROM python:3.7-alpine
WORKDIR /opt/2miners-exporter
COPY ./requirements.txt .
RUN apk --no-cache add --virtual build-dependencies build-base \
    && pip install -r requirements.txt \
    && apk del build-dependencies
COPY ./2miners.py .

ENTRYPOINT ["python3", "2miners.py"]
