#!/bin/sh

sh auth.sh docker-compose.yml
docker compose up -d

docker exec {{cookiecutter.project_name}}-rstudio-1 apt-get update
docker exec {{cookiecutter.project_name}}-rstudio-1 apt-get install -y \
libcurl4-openssl-dev libssl-dev libjq-dev libprotobuf-dev protobuf-compiler \
make libgeos-dev libglpk40 libudunits2-dev libgdal-dev gdal-bin libproj-dev libv8-dev

make write-lib
make docker-stop

nb_id=$(id -u)
sed -i '' -e s/${nb_id}/YOUR_ID/ docker-compose.yml
