#!/bin/sh

set -e

apk add libjpeg-turbo-dev gcc musl-dev
cp -r /usr/lib/* /srv/lib

apk add git make

export INSTALL_PREFIX=/srv

git clone https://github.com/ImageMagick/ImageMagick.git
cd ImageMagick
./configure -prefix $INSTALL_PREFIX
make -j
make install
