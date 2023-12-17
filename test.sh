#!/bin/sh

# Use Node.js 16.x from NVM
source ~/.nvm/nvm.sh  # Load NVM
nvm use 16            # Use Node.js 16.x as the active version

set -e # exit immediately if newman complains
trap 'kill $PID' EXIT # kill the server on exit

./run.sh &
PID=$! # record the PID

newman run forum_multiple_posts.postman_collection.json -e env.json # use the env file
newman run forum_post_read_delete.postman_collection.json -n 50 # 50 iterations
