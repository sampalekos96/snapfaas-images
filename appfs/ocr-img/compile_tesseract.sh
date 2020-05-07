#!/bin/sh

set -e

apk add git alpine-sdk cmake make autoconf libtool automake libjpeg-turbo-dev tiff-dev libpng-dev zlib-dev giflib-dev libwebp-dev

export INSTALL_PREFIX=/srv/tesseract

wget https://github.com/DanBloomberg/leptonica/releases/download/1.78.0/leptonica-1.78.0.tar.gz
tar xzf leptonica-1.78.0.tar.gz
cd leptonica-1.78.0
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$INSTALL_PREFIX -DBUILD_PROG=1 ..
make -j
make install
cd /tmp

wget https://github.com/tesseract-ocr/tesseract/archive/4.1.0.tar.gz
tar xzf 4.1.0.tar.gz
cd tesseract-4.1.0
git apply /srv/include-time-h.patch
mkdir build
cd build
PKG_CONFIG_PATH=$INSTALL_PREFIX/lib/pkgconfig cmake -DCMAKE_INSTALL_PREFIX=$INSTALL_PREFIX ..
make -j
make install

mkdir -p /srv/tesseract/share/tessdata
wget -O /srv/tesseract/share/tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata/raw/3.04.00/eng.traineddata

cp /usr/lib/libjpeg* /srv/tesseract/lib
cp /usr/lib/libpng* /srv/tesseract/lib
cp /usr/lib/libtiff* /srv/tesseract/lib
cp /usr/lib/libwebp* /srv/tesseract/lib
cp /usr/lib/libgif* /srv/tesseract/lib

