#!/bin/bash

cd $(dirname $(readlink -f "$0"))

if [ -e ".env" ]
then
    source .env
else
    echo "Missing .env file with ZEROTIER_CENTRAL_TOKEN"
    exit 1
fi

if [ -z "$ZEROTIER_CENTRAL_TOKEN" ]
then
    echo ".env file does not contain a ZEROTIER_CENTRAL_TOKEN"
    exit 2
fi

if [ -e ".venv/bin/activate" ]
then
    source .venv/bin/activate
else
    echo ".venv not found, creating one…"
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
fi

export ZEROTIER_CENTRAL_TOKEN

./zerotier-info.py "$@"
