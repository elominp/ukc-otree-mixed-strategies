FROM debian:latest

RUN apt-get update && apt-get install -y build-essential make wget

RUN wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz

RUN tar -xz Python* && cd Python* && echo "WIP"