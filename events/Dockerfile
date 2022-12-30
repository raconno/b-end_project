FROM python:3.8.3-slim-buster
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /events
COPY . .
CMD ["uvicorn", "controller:app", "--host", "0.0.0.0", "--port", "81"]