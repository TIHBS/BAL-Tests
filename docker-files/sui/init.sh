curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > installer.sh
chmod +x installer.sh
./installer.sh -q -y
source "$HOME/.cargo/env"
cargo install --locked --git https://github.com/MystenLabs/sui.git --branch devnet sui
