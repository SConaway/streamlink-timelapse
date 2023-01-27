#! /usr/bin/env bash

set -eux

# apt update

apt install -y --no-install-recommends ffmpeg
# apt install -y --no-install-recommends streamlink ffmpeg bc

# rm -rf /var/lib/apt/lists/*

pip install -r requirements.txt
