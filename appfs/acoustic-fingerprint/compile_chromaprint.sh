#!/bin/sh

set -e

apk add ffmpeg-libs libstdc++ libgcc musl
cp -r /usr/lib/* /srv/lib

apk add git alpine-sdk cmake make autoconf libtool automake ffmpeg-dev

export INSTALL_PREFIX=/srv

wget https://github.com/acoustid/chromaprint/releases/download/v1.5.0/chromaprint-1.5.0.tar.gz
tar xzf chromaprint-1.5.0.tar.gz
cd chromaprint-v1.5.0
cmake -DCMAKE_INSTALL_PREFIX=$INSTALL_PREFIX -DBUILD_TOOLS=ON -DCMAKE_BUILD_TYPE=Release .
make -j
make install
