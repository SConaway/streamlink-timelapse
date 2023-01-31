#! /usr/bin/env python3

# parse arg[1]
# == stream: run bash stream script
# == process: run py function

import datetime
import os
import sys
import subprocess
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.

config = {}
# 'final_frame_rate': 30,
# 'frame_interval': 0.25,  # seconds
# 'tmp_dir': './tmp',
# 'out_dir': './out'
# 'check_interval': 5,  # minutes
# 'b2_application_key_id': "<>",
# 'b2_application_key': "<>",
# "b2_bucket_name": "<>"

env = [
    ('final_frame_rate', 30),  # fps
    ('frame_interval', 60),    # seconds
    ('tmp_dir', '/tmp'),       # path
    ('out_dir', '/out'),       # path
    ('url', None),             # url
    ('check_interval', 5),     # minutes
    ('b2_application_key_id', None),  # b2 application key id
    ('b2_application_key', None),     # b2 application key
    ('b2_bucket_name', None),         # b2 bucket name
]

for key, default in env:
    if key.upper() in os.environ:
        v = os.environ[key.upper()]
        print(f"Using environment variable {key}: {v}")
        if v.replace('.', '').isnumeric():
            if '.' in v:
                v = float(v)
            else:
                v = int(v)
        config[key] = v
    else:
        if default:
            print(f"Using default value for {key}: {default}")
            config[key] = default
        else:
            print(f"Missing required environment variable {key}")
            sys.exit(2)

config['frame_rate'] = float(1) / config['frame_interval']

print(config)


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
            ['bash', 'stream.sh', str(config['frame_rate']), f"{config['tmp_dir']}/{date}.ts", config['url']])

        print(p)
        if p.returncode != 0:
            print('Error running stream.sh, check logs')
            sys.exit(1)

        # create file named date.ts.done, write done at current time
        with open(f"{config['tmp_dir']}/{date}.ts.done", "w") as f:
            f.write(
                f"done at {datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}")


checkFilesPreStream(config)
stream(config)
