FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip uninstall -y redis \
    && rm -rf /usr/local/lib/python3.12/site-packages/redis* \
    && rm -rf /usr/local/lib/python3.12/site-packages/redis-*.dist-info

RUN pip install --no-cache-dir redis==7.1.0

COPY . .

CMD ["python", "main.py"]