FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir flask pandas pyarrow

COPY server.py /app/server.py

CMD ["python", "server.py"]
