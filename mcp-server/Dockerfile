FROM python:3.11-slim

WORKDIR /app

# نصب پیش‌نیازها و کلاینت سبک داکر برای دسترسی به داکر هاست
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    procps \
    && curl -fsSL https://download.docker.com/linux/static/stable/x86_64/docker-24.0.7.tgz | tar -xz -C /tmp \
    && mv /tmp/docker/docker /usr/local/bin/ \
    && rm -rf /tmp/docker /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

ENV PORT=8000
ENV HOST=0.0.0.0

EXPOSE 8000

CMD ["python", "server.py"]
