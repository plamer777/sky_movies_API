FROM python:3.10-slim
WORKDIR /sky_movies
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python3.10 create_tables.py
RUN python3.10 load_fixtures.py
CMD gunicorn -b 0.0.0.0:5000 --workers=2 --threads=2 run:app