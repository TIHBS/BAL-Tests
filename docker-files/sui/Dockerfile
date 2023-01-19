FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR app

RUN apt-get update \
  && apt-get install -y curl git-all libssl-dev libclang-dev cmake pkg-config

ADD init.sh /app/init.sh
RUN chmod +x /app/init.sh