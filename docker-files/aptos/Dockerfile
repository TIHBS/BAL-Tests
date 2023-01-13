FROM ubuntu:22.04

WORKDIR app

ADD aptos /root/bin/aptos
ADD init.sh /app/init.sh

RUN chmod +x /app/init.sh

ENV PATH="$PATH:/root/bin"

EXPOSE 8080 8081

# CMD ["aptos" ,"config", "set-global-config", "--config-type", "global"]
# CMD ["aptos","init", "--faucet-url", "http://localhost:8081","--private-key", "0x7e34dd73fd923367d3367aee586cebd9ec6f59376739df42e4e4d40b5d3f1157", "--rest-url", "http://localhost:8080", "--profile", "local", "--network", "local"]
ENTRYPOINT ["sh", "/app/init.sh"]
CMD ["aptos", "node", "run-local-testnet", "--with-faucet"]

