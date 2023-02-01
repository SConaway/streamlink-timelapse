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
import b2sdk.v2 as b2


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


def process(config, bucket, all=False, file=None):
    # print current date/time in blue text on a yellow background
    print('\033[43m\033[34mStart Time:' + datetime.datetime.now().strftime(
        '%Y-%m-%dT%H-%M-%S') + '\033[0m')

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

    print('processing:', files_to_process)

    for file in files_to_process:
        newName = file.replace('.ts', '.mp4')
        p = subprocess.run(
            ['bash', 'ffmpeg.sh', str(config['final_frame_rate']), f"{config['tmp_dir']}/{file}", f"{config['out_dir']}/{newName}"])

        # if success
        if p.returncode == 0:
            # uploaded_file =
            bucket.upload_local_file(
                local_file=f"{config['out_dir']}/{newName}",
                file_name=newName,
                # file_infos=metadata,
            )

            # print(uploaded_file)

            # remove file and its .done file if exists
            os.remove(f"{config['tmp_dir']}/{file}")
            if os.path.exists(f"{config['tmp_dir']}/{file}.done"):
                os.remove(f"{config['tmp_dir']}/{file}.done")

            os.remove(f"{config['out_dir']}/{newName}")


# wait some time for the stream script to
# mark any files with a `.done` file as done
time.sleep(5)

info = b2.InMemoryAccountInfo()
b2_api = b2.B2Api(info)
b2_api.authorize_account(
    "production", config['b2_application_key_id'], config['b2_application_key'])

bucket = b2_api.get_bucket_by_name(config['b2_bucket_name'])

while True:
    process(config, all=False, bucket=bucket)
    print(f"Sleeping for {config['check_interval']} minutes")
    time.sleep(config['check_interval']*60)
