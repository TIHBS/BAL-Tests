FROM rust:1.65

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR app

RUN apt-get update \
  && apt-get install -y libclang-dev

RUN cargo install --locked --git https://github.com/MystenLabs/sui.git --branch devnet sui
#
#ADD files/init.sh /app/init.sh
#RUN chmod +x /app/init.sh