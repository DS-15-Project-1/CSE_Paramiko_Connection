FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir flask pandas pyarrow

COPY server.py /app/server.py

EXPOSE 5000

CMD ["python", "server.py"]
