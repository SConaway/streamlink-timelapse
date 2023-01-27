# streamlink-timelapse

This is a program to create a timelapse of a stream. It uses
[streamlink](https://streamlink.github.io/) to download the stream and
[ffmpeg](https://ffmpeg.org/) to create the timelapse. The main script is
written in Python and configuration is done by environment variables.

The videos created are restarted every week and saved to `/output` in the container.
