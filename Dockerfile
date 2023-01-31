# FROM debian:bookworm-slim

FROM python:3.11-slim-bullseye

WORKDIR /app

# RUN apt update && apt install -y python
RUN apt update && \
    apt install -y --no-install-recommends ffmpeg && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# COPY setup.sh /setup.sh

# RUN /setup.sh

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY *.sh /app/

COPY *.py /app/

ENTRYPOINT ["python"]
