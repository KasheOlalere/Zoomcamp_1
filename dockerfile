FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY green_taxi.py green_taxi.py

ENTRYPOINT [ "python", "green_taxi.py" ]