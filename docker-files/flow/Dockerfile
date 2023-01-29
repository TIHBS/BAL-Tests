FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR app

RUN apt-get update \
  && apt-get install -y curl

RUN sh -ci "$(curl -fsSL https://raw.githubusercontent.com/onflow/flow-cli/master/install.sh)"
RUN echo 'export PATH="$PATH:/root/.local/bin"' >>~/.bashrc
CMD ["/root/.local/bin/flow", "emulator", "--contracts", "true"]