sui genesis
# gas_address=$(sui client gas | sed -n '3 p' | cut -d' ' -f2,5)
sui client transfer-sui --amount 1000000 --to 0xa7d262f7599441aef3499d7f6b5b69ef35610259 --sui-coin-object-id $(sui client gas | sed -n '3 p' | cut -d' ' -f2,5) --gas-budget 1000
