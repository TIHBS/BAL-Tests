FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR app

RUN apt-get update \
  && apt-get install -y curl

ADD init.sh /app/init.sh
ADD flow.json /app/flow.json
ADD contracts /app/contracts
RUN chmod +x /app/init.sh