#!/bin/sh

nb_id=$(id -u)
sed -i '' -e s/YOUR_ID/${nb_id}/ $1
