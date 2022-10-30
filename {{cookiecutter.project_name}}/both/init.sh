#!/bin/sh

sh auth.sh docker-compose.yml
docker compose up -d

sh linux_deps.sh

make write-lib
sh jupyter.sh stop
sh rstudio.sh stop

nb_id=$(id -u)
sed -i '' -e s/${nb_id}/YOUR_ID/ docker-compose.yml
