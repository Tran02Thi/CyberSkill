#!/bin/bash

set -e

VERSION_APP=1.0
STACK_NAME=lemp

sudo docker build --rm -t app:$VERSION_APP ./monitoring/backend/ || exit 1

docker stack rm $STACK_NAME
sleep 25

echo "Build docker stack ..."

cd monitoring

sudo docker stack deploy -c docker-compose.yml $STACK_NAME || exit 1

sudo docker ps

echo "Docker containers are up and running!"



