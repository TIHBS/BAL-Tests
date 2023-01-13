# Setup blockchain nodes

## Aptos

### Download and unzip binary

```bash
wget https://github.com/aptos-labs/aptos-core/releases/download/aptos-cli-v1.0.4/aptos-cli-1.0.4-Ubuntu-22.04-x86_64.zip
unzip aptos-cli-1.0.4-Ubuntu-22.04-x86_64.zip
 ```

### Build docker container

```bash
docker build . -f Dockerfile -t aptos
```

### Start node

```bash
docker run --name aptos -p 8080:8080 -p 8081:8081 -it --rm aptos
```