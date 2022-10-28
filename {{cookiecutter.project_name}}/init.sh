#!/bin/sh

sh auth.sh docker-compose.yml
docker compose up -d
make write-lib

if [[ -e jupyter.sh ]]; then
    sh jupyter.sh stop
fi

if [[ -e jupyter.sh ]]; then
    sh rstudio.sh stop
fi

nb_id=$(id -u)
sed -i '' -e s/${nb_id}/YOUR_ID/ docker-compose.yml
