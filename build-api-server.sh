#!/usr/bin/env bash

docker build -f Dockerfile.api-server --tag briandeheus/api-server:$1 .
docker push briandeheus/api-server:$1
