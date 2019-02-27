#!/usr/bin/env bash

docker build -f Dockerfile.socket-server --tag briandeheus/socket-server:$1 .
docker push briandeheus/socket-server:$1
