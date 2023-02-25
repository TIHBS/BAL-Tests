FROM node:16.15.1

WORKDIR /app

RUN git clone https://github.com/TIHBS/bal-sui-plugin.git

WORKDIR /app/bal-sui-plugin

COPY .env .

RUN npm install

CMD [ "npm", "start" ]

# Expose port 7878 to the host
EXPOSE 7878