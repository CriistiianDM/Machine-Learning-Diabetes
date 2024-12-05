#!/bin/bash
set -e

# Verdaderos sistemas distribuidos, no es como ese fake de docker compose

docker-machine create -d virtualbox --virtualbox-memory=1536 \
    --virtualbox-cpu-count=1 --virtualbox-disk-size=40960 \
    --virtualbox-no-vtx-check s3-local

docker-machine create -d virtualbox --virtualbox-memory=1536 \
    --virtualbox-cpu-count=1 --virtualbox-disk-size=40960 \
    --virtualbox-no-vtx-check machine-learning