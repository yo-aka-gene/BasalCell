#!/bin/sh

sh auth.sh docker-compose.yml
docker compose up -d
make write-lib
make docker-stop

nb_id=$(id -u)
sed -i '' -e s/${nb_id}/YOUR_ID/ docker-compose.yml
