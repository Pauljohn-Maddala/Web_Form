#!/bin/sh

set -e # exit immediately if newman complains
trap 'kill $PID' EXIT # kill the server on exit

./run.sh &
PID=$! # record the PID of the server

# Test creating multiple posts
newman run forum_multiple_posts.postman_collection.json -e env.json

# Test reading and deleting posts, 50 iterations
newman run forum_post_read_delete.postman_collection.json -n 50

