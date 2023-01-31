#! /usr/bin/env bash

set -eux

# debug: print args
echo "args: $@"

if [ $# -ne 3 ]; then
    echo "Usage: $0 <FR> <output_path> <url>"
    exit 2
fi

FRAME_RATE=$1
OUTPUT_PATH=$2
URL=$3

# print fr, op, url, start time in green on red
echo -e "\e[1;37;41mFRAME_RATE=$FRAME_RATE\e[0m"
echo -e "\e[1;37;41mOUTPUT_PATH=$OUTPUT_PATH\e[0m"
echo -e "\e[1;37;41mURL=$URL\e[0m"
echo -e "\e[1;37;41mSTART TIME: $(date)\e[0m"

if command -v terminal-notifier &>/dev/null; then
    terminal-notifier -title "stream" -message "START TIME: $(date)"
fi

# make sure that streamlink is installed
if ! command -v streamlink &>/dev/null; then
    echo "streamlink could not be found"
    exit 1
fi
if ! command -v ffmpeg &>/dev/null; then
    echo "ffmpeg could not be found"
    exit 1
fi

# TODO: set this to be a week
# while true; do
streamlink --loglevel warning --stdout "$URL" best | ffmpeg -loglevel warning -y -i pipe:0 -r "$FRAME_RATE" -t 02:00:00 -vf drawtext='fontfile=FreeSans.ttf:text=%{localtime\\:%b %d %Y %I %p}' "$OUTPUT_PATH"
# done

# print end time in green on red
echo -e "\e[1;37;41mEND TIME: $(date)\e[0m"

if command -v terminal-notifier &>/dev/null; then
    terminal-notifier -title "stream" -message "END TIME: $(date)"
fi
