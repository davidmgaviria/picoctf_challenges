#!/bin/bash

set -e

# start app & load flag (then wipe file)
python3 /app/app.py &
sleep 0.5

# start ssh service
service ssh start
socat tcp-listen:5555,reuseaddr,fork tcp:localhost:22

