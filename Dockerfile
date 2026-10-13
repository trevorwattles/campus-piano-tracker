FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY setup.sql setupData.sql ./
COPY app ./app
# SQLite lives inside the container; it is rebuilt from the .sql files on every start
ENV DB_PATH=/srv/data/pianos.sqlite
EXPOSE 8000
CMD ["python", "app/server.py"]
