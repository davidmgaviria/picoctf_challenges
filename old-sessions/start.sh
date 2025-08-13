#!/bin/bash

# Generate users (will keep trying until web page is active)
python3 /app/generate_users.py > generation_log.txt &

# Start app
python3 /app/app.py
