#!/bin/bash

echo "Setting up the songbook build environment..."

apt-get install -y build-essential ghostscript

cd /tmp
git clone https://github.com/leesavide/abcm2ps
cd abcm2ps
./configure
make
make install