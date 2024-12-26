#!/bin/bash

# Geocoder api (stand-alone http server. single process)
git pull

lsof -ti:4002 | xargs kill -9

cd ~/projects/geocoder-kr
source venv/bin/activate
echo 'Starting...'

export FLASK_ENV=production
echo | nohup python api_fast.py 4002 >> log/geocode-api.log &

sleep 1
echo 'Started'

