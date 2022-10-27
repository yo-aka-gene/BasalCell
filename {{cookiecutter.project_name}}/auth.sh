#!/bin/sh

git update-index --skip-worktree $1
nb_id=$(id -u)
sed -i '' -e s/YOUR_ID/${nb_id}/ $1
