#!/bin/sh

docker buildx build --platform linux/amd64 --tag tea.shupogaki.org/yuruc3/snmpython:v0  --debug --push .
