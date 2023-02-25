# Setup blockchain nodes

### Build docker container

```bash
docker build . -f Dockerfile -t aptos
```

### Start node

```bash
docker run --name aptos -p 9002:8080 -p 9003:8081 -it --rm aptos
```

Open a new terminal and run the below command

```bash
docker exec -it aptos bash /app/init.sh
```