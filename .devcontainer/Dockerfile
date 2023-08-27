FROM mcr.microsoft.com/devcontainers/base:jammy

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
LABEL org.opencontainers.image.source https://github.com/sandor-juhasz/songbooks

