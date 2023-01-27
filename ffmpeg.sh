#! /usr/bin/env bash

# set -eux

# debug: print args
echo "args: $@"

if [ $# -ne 3 ]; then
    echo "Usage: $0 <FR> <input path> <output_path>"
    exit 2
fi

FRAME_RATE=$1
INPUT_PATH=$2
OUTPUT_PATH=$3

# print fr, ip, op, start time in red on green
echo -e "\e[1;37;42mFRAME_RATE=$FRAME_RATE\e[0m"
echo -e "\e[1;37;42mINPUT_PATH=$INPUT_PATH\e[0m"
echo -e "\e[1;37;42mOUTPUT_PATH=$OUTPUT_PATH\e[0m"
echo -e "\e[1;37;42mSTART TIME: $(date)\e[0m"

if command -v terminal-notifier &>/dev/null; then
    terminal-notifier -title "ffmpeg" -message "START TIME: $(date)"
fi

ffmpeg -loglevel warning -y -r "$FRAME_RATE" -i "$INPUT_PATH" -movflags +faststart -r "$FRAME_RATE" "$OUTPUT_PATH"

exitcode=$?

if [ $exitcode -ne 0 ]; then
    echo "ffmpeg exited with code $exitcode"
    terminal-notifier -title "ffmpeg" -message "ffmpeg exited with code $exitcode at $(date)"
    exit $exitcode
else
    # remove file and file.done
    rm -f "$INPUT_PATH" "$INPUT_PATH.done"
fi

# print end time in red on green
echo -e "\e[1;37;42mEND TIME: $(date)\e[0m"

if command -v terminal-notifier &>/dev/null; then
    terminal-notifier -title "ffmpeg" -message "END TIME: $(date)"
fi
