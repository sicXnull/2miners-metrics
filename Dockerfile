FROM python:3.7-alpine
WORKDIR /home/sic/
COPY ./requirements.txt .
RUN apk --no-cache add --virtual build-dependencies build-base \
    && pip install -r requirements.txt \
    && apk del build-dependencies
COPY ./main.py .

ENTRYPOINT ["python3", "main.py"]
