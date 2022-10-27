#!/bin/sh

nb_id=$(id -u)
sed -i '' -e s/YOUR_ID/${nb_id}/ $1
docker compose up -d
docker start build_both-jupyterlab-1
make write-lib
# make terminate
