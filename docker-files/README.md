```bash
docker-compose up --no-deps --build aptos flow bal bal_callback_handler
```

```bash
# Flow node
docker exec -it flow bash
flow accounts add-contract contracts/Example.cdc
exit

# Aptos node
docker exec -it aptos bash /app/init.sh
```