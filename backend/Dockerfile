FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN sed -i'.bak' 's/$/ contrib/' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y ttf-mscorefonts-installer fontconfig gettext && \
    pip3 install -r requirements.txt --no-cache-dir && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

CMD ["gunicorn", "api_foodgram.wsgi:application", "--bind", "0:8000" ]
