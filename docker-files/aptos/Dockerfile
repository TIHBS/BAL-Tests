FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir /root/bin

WORKDIR app
RUN apt-get update \
  && apt-get install -y git wget unzip

RUN wget -q https://github.com/aptos-labs/aptos-core/releases/download/aptos-cli-v1.0.4/aptos-cli-1.0.4-Ubuntu-22.04-x86_64.zip
RUN unzip aptos-cli-1.0.4-Ubuntu-22.04-x86_64.zip -d aptos
RUN mv aptos/aptos /root/bin/aptos && rmdir aptos

RUN git clone -b aptos-node-v1.2.5 https://github.com/aptos-labs/aptos-core.git

ADD init.sh /app/init.sh

RUN chmod +x /app/init.sh

ENV PATH="$PATH:/root/bin"

EXPOSE 8080 8081

CMD ["aptos", "node", "run-local-testnet", "--with-faucet"]

