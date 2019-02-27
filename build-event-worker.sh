#!/usr/bin/env bash

docker build -f Dockerfile.event-worker --tag briandeheus/event-worker:$1 .
docker push briandeheus/event-worker:$1
