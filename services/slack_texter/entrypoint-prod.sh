#!/bin/sh
echo "get the party started"

gunicorn -b 0.0.0.0:5000 manage:app