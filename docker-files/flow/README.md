```bash
docker build . -f Dockerfile -t flow
```

```bash
docker run -rm -it -p 3569:3569 -p 8888:8888 --name flow bash
./init.sh
source ~/.bashrc
```

```bash
docker run --rm -it -p 3569:3569 -p 8888:8888 --network host --name flow flow bash
flow emulator --contracts true
```

```bash
flow accounts add-contract contracts/hello_world.cdc
```