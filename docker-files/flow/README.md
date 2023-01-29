```bash
docker build . -f Dockerfile -t flow
```

```bash
docker run --rm -it -p 3569:3569 -p 8888:8888 --network host -v $PWD/files:/app/ --name flow flow bash
#./init.sh
#source ~/.bashrc
flow emulator --contracts true
```

```bash
flow accounts add-contract contracts/hello_world.cdc

flow accounts remove-contract Example
flow accounts add-contract contracts/Example.cdc

```