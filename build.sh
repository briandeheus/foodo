#!/usr/bin/env bash

build-api-server.sh $1

docker build -f Dockerfile.event-worker --tag briandeheus/event-worker:$1 .

docker push briandeheus/event-worker:$1
docker push briandeheus/socket-server:$1
