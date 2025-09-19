FROM python:3.11-slim

WORKDIR /app

# Install build deps for psycopg2
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
ENV PATH="/root/.local/bin:$PATH"

CMD ["python", "src/main.py"]
