from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve import PrivateKey, PublicKey

# Generate new Keys
privateKey = PrivateKey()
publicKey = privateKey.publicKey()

print(privateKey.toPem())
print(publicKey.toDer())
