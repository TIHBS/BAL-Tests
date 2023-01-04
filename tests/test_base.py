import base64
import json
import os
import unittest
import random
from typing import Any
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey, secp256k1
import requests


class TestBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestBase, self).__init__(*args, **kwargs)

    def setUp(self):
        self.server_url = "http://localhost:9091"
        self.plugin_dir = "/home/ash/Softwares/apache-tomcat-8.5.84/plugins"
        self.signers = self.read_signers()

    def upload_plugin(self):
        url = f"{self.server_url}/webapi/plugins/"

        payload = {}
        files = [
            ('file', ('file', open(self.plugin_path, 'rb'), 'application/octet-stream'))
        ]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        self.assertEqual(response.status_code, 200)

    def upload_connection_profile(self, body: dict):
        url = f"{self.server_url}/webapi/configure/"

        payload = {}
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def get_pending_transactions(self) -> Any:
        url = f"{self.server_url}/webapi?/message"

        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "GetPendingTransactions",
            "id": 1,
            "params": {}
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['result']

    def try_cancel_invocation(self, correlationId: str, signature: str, signer: str) -> bool:
        url = f"{self.server_url}/webapi?/message"

        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "TryCancelInvocation",
            "id": 1,
            "params": {
                "signature": signature,
                "correlationIdentifier": correlationId,
                "signer": signer
            }
        })
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['result']

    def try_replace_invocation(self, body: dict) -> bool:
        url = f"{self.server_url}/webapi?/message"

        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "TryReplaceInvocation",
            "id": random.randint(0, 10000),
            "params": body
        })
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['result']

    def invoke(self, request_id: int, body: dict, url: str):
        template = {
            "jsonrpc": "2.0",
            "method": "Invoke",
            "id": request_id,
            "params": body
        }

        payload = json.dumps(template)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    def sign_invocation(self, correlation_id: str, signature: str, signer: str):
        url = f"{self.server_url}/webapi?/message"

        body = {
            "jsonrpc": "2.0",
            "method": "SignInvocation",
            "id": 1,
            "params": {
                "signature": signature,
                "signer": signer,
                "correlationIdentifier": correlation_id
            }

        }

        payload = json.dumps(body)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()['result']

    def read_signers(self):
        keys_file = os.path.join("assets", "keys.json")

        result = {}
        with open(keys_file, 'r') as f:
            signers = json.load(f)
            for signer in signers:
                base64_message = signer["privateKey"]
                base64_bytes = base64_message.encode('ascii')
                message_bytes = base64.b64decode(base64_bytes)

                privateKey = PrivateKey.fromDer(message_bytes)
                publicKey = privateKey.publicKey()
                pem_public_key = publicKey.toPem()
                publicK = pem_public_key.replace("\n", '')
                publicK = publicK.replace('-----BEGIN PUBLIC KEY-----', "")
                publicK = publicK.replace('-----END PUBLIC KEY-----', '')
                assert publicK == signer['publicKey']

                result[signer["name"]] = {
                    'publicKey': publicKey,
                    'privateKey': privateKey,
                    'public_key_str' : signer['publicKey']
                }
        return result
