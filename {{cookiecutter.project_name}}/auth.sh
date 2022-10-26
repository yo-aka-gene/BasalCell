#!/bin/sh

get_id=$(id)
nb_id=${get_id[@]:4:3}
sed -i '' -e s/YOUR_ID/${nb_id}/ $1
