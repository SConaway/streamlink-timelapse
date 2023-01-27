# FROM debian:bookworm-slim

FROM python:3.11-slim-bullseye

# RUN apt update && apt install -y python
RUN apt update && \
    apt install -y --no-install-recommends ffmpeg && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# COPY setup.sh /setup.sh

# RUN /setup.sh

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY *.sh /

COPY main.py /

ENTRYPOINT ["python", "/main.py"]
