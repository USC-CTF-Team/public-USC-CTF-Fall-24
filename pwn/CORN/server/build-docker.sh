#!/bin/sh

docker build . -t corn && \
    docker run -p 9999:9999 -it corn
