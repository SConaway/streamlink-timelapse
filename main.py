#! /usr/bin/env python3

# parse arg[1]
# == stream: run bash stream script
# == process: run py function

import datetime
import os
import sys
import subprocess
from dotenv import load_dotenv
import time


def help():
    print('Usage: main.py <stream|process|check>')


def get_config():
    load_dotenv()  # take environment variables from .env.

    config = {}
    # 'final_frame_rate': 30,
    # 'frame_interval': 0.25,  # seconds
    # 'tmp_dir': './tmp',
    # 'out_dir': './out'
    # 'check_interval': 5,  # minutes

    env = [
        ('final_frame_rate', 30),  # fps
        ('frame_interval', 60),    # seconds
        ('tmp_dir', './tmp'),       # path
        ('out_dir', './out'),       # path
        ('url', None),             # url
        ('check_interval', 5),     # minutes
    ]

    for key, default in env:
        if key.upper() in os.environ:
            config[key] = os.environ[key.upper()]
        else:
            if default:
                print(f"Using default value for {key}: {default}")
                config[key] = default
            else:
                print(f"Missing required environment variable {key}")
                sys.exit(2)

    config['frame_rate'] = float(1) / config['frame_interval']

    print(config)
    return config


def checkFilesPreStream(config):
    # check if tmp dir exists
    if not os.path.exists(config['tmp_dir']):
        os.mkdir(config['tmp_dir'])

    # for each temp file
    # check if file.done exists
    # if not, create it

    dir = os.listdir(config['tmp_dir'])
    files = [f for f in dir if f.endswith('.ts')]
    for file in files:
        if not os.path.exists(f"{config['tmp_dir']}/{file}.done"):
            with open(f"{config['tmp_dir']}/{file}.done", "w") as f:
                f.write("done at unknown time")


def stream(config):
    while True:
        date = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        p = subprocess.run(
            ['bash', 'stream.sh', str(config['frame_rate']), f"./tmp/{date}.ts", config['url']])

        print(p)
        if p.returncode != 0:
            print('Error running stream.sh, check logs')
            sys.exit(1)

        # create file named date.ts.done, write done at current time
        with open(f"./tmp/{date}.ts.done", "w") as f:
            f.write(
                f"done at {datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}")

        # process(config, file=f"{date}.mp4")
        # add process job to scheduler
        # scheduler.add_job(
        #     process, args=[config, False, f"{date}.mp4"], id=f"{date}.mp4")  # , executor='processpool')

        # print(scheduler.get_jobs())
        # break


def process(config, all=False, file=None):
    # list files in tmp_dir
    # for each file print name
    dir = os.listdir(config['tmp_dir'])
    # print(dir)

    files_to_process = [file]
    if all:
        files_to_process = [f for f in dir if f.endswith('.ts')]
    elif not file:
        files_to_process = [f.split('.done')[0]
                            for f in dir if f.endswith('.ts.done')]

    print(files_to_process)

    for file in files_to_process:
        subprocess.run(
            ['bash', 'ffmpeg.sh', str(config['final_frame_rate']), f"{config['tmp_dir']}/{file}", f"{config['out_dir']}/{file.replace('.ts', '.mp4')}"])

        # remove file and its .done file if exists
        # os.remove(f"{config['tmp_dir']}/{file}")
        # if os.path.exists(f"{config['tmp_dir']}/{file}.done"):
        #     os.remove(f"{config['tmp_dir']}/{file}.done")


config = get_config()

if len(sys.argv) != 2:
    print('Invalid argument')
    help()
    sys.exit(2)

# TODO: process any files at start
# process(config, all=True)

if sys.argv[1] == 'stream':
    checkFilesPreStream(config)
    stream(config)
elif sys.argv[1] == 'process':
    # process every check_interval minutes
    while True:
        process(config, all=False)
        print(f"Sleeping for {config['check_interval']} minutes")
        time.sleep(config['check_interval']*60)
elif sys.argv[1] == 'check':
    checkFilesPreStream(config)
else:
    print('Invalid argument')
    help()
    sys.exit(2)
