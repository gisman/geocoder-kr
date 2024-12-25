#!/bin/bash

# Geocoder api (stand-alone http server. single process)

lsof -ti:4002 | xargs kill -9

sleep 1
echo 'Stopped'

