#!/bin/bash
set -e

docker-machine create \
    --driver generic \
    --generic-ip-address=192.168.1.43 \
    --generic-ssh-user=cristiank \
    --generic-ssh-key=/home/cristiank/.ssh/machine-s3-local/id_rsa \
    s3-local

docker-machine create \
    --driver generic \
    --generic-ip-address=192.168.1.44 \
    --generic-ssh-user=cristiank \
    --generic-ssh-key=/home/cristiank/.ssh/machine-learning/id_rsa \
    machine-learning