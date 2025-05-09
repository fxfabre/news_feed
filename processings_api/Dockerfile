FROM python:3.12.4-slim-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc build-essential \
 && pip install --disable-pip-version-check --no-cache-dir -r requirements.txt \
 && apt-get purge -y gcc && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

COPY config /app/config/
COPY src /app/src/

EXPOSE 5000

CMD [ \
    "gunicorn", \
    "--config", "config/gunicorn.conf.py", \
    "--worker-tmp-dir", "/dev/shm", \
    "--log-level", "info", \
    "src.fastapi_app:app" \
]
