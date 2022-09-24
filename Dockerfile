FROM python:3.10-alpine
WORKDIR /home/
COPY ./requirements.txt .
RUN apk --no-cache add --virtual build-dependencies build-base \
    && pip install -r requirements.txt \
    && apk del build-dependencies
COPY ./exporter.py .

ENTRYPOINT ["python3", "exporter.py"]
