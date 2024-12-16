#!/bin/bash

# Geocoder api (stand-alone http server. single process)
git pull

lsof -ti:4001 | xargs kill -9

cd ~/projects/geocoder-api
source venv/bin/activate
echo 'Starting...'

export FLASK_ENV=production
echo | nohup python src/api.py >> log/geocode-api.log &

sleep 1
echo 'Started'

