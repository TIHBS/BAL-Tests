FROM ubuntu:22.04

WORKDIR app

ADD aptos /root/bin/aptos
ADD init.sh /app/init.sh
ADD aptos-core /app/aptos-core

RUN chmod +x /app/init.sh

ENV PATH="$PATH:/root/bin"

EXPOSE 8080 8081

CMD ["aptos", "node", "run-local-testnet", "--with-faucet"]

