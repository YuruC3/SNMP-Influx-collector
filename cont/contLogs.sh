#!/bin/sh

while true; do
    docker container logs snmpython-dev -f

    # Added to have time to ctrl+C
    sleep 0.5
done