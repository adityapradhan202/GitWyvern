#!/bin/bash

WORKDIR="./workdir"

if [ -d "$WORKDIR" ]; then
    echo "Force removing workdir..."
    rm -rf "$WORKDIR"
fi

mkdir "$WORKDIR"
