CONTAINER_ALREADY_STARTED="CONTAINER_ALREADY_STARTED_PLACEHOLDER"
if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
  touch $CONTAINER_ALREADY_STARTED
  echo "-- First container startup --"
  aptos config set-global-config --config-type global
  aptos init --faucet-url http://localhost:8081 --private-key 0x7e34dd73fd923367d3367aee586cebd9ec6f59376739df42e4e4d40b5d3f1157 --rest-url http://localhost:8080 --profile default --network local
  aptos account fund-with-faucet --account default

  public_key=0x9f709239a4caf988527df46b7dca3797b740e408e48aa713e79a87fe85a53c4d
  (cd /app/aptos-core/aptos-move/move-examples/hello_blockchain && aptos move publish --named-addresses hello_blockchain=$public_key --assume-yes)
else
  echo "-- Not first container startup --"
fi
