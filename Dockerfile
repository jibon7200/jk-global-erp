FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-ben \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-noto-core \
    fonts-noto-color-emoji \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo "=== Checking static folder ===" && ls -la /app/static/ && ls -la /app/static/css/ || echo "STATIC FOLDER NOT FOUND"

ENV TESSERACT_CMD_PATH=/usr/bin/tesseract
ENV SECRET_KEY=dummy-key-only-used-during-docker-build-not-in-production
ENV DEBUG=False
ENV ALLOWED_HOSTS=localhost

RUN python manage.py collectstatic --noinput

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]