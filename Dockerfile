FROM ubuntu:latest

RUN <<EOF
    apt-get update
    apt-get install -y build-essential ghostscript abcmidi git

    cd /tmp
    git clone https://github.com/leesavide/abcm2ps
    cd abcm2ps
    ./configure
    make
    make install
EOF
