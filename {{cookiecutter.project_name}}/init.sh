#!/bin/sh

sh auth.sh docker-compose.yml
docker compose up -d
make write-lib
make docker-stop
