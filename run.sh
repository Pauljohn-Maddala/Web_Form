#!/bin/bash
export FLASK_APP=server_v2.py  # replace with your Flask app file name
export FLASK_ENV=development
exec flask run
