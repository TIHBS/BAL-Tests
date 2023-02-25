import base64
import json
import os
import string
import unittest
import random
from typing import Any
from ellipticcurve.privateKey import PrivateKey
import requests
from abc import ABC, abstractmethod
from ellipticcurve.ecdsa import Ecdsa
from requests import Response
from config import config


class TestBase(ABC, unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestBase, self).__init__(*args, **kwargs)

    def setUp(self):
        self.server_url = config["BAL_URL"]
        self.signers = self.read_signers()
        self.plugin = None

    def upload_plugin(self):
        with  open(self.plugin_path, 'rb') as f:
            url = f"{self.server_url}/webapi/plugins/"
            f_name = self.plugin_path.split(os.sep)[-1]

            payload = {}
            files = [
                ('file', (f_name, f, 'application/octet-stream'))
            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

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
            "method": "Get",
            "id": 1,
            "params": {}
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['result']

    def try_cancel_invocation(self, correlationId: str, signature: str, signer: str) -> Response:
        url = f"{self.server_url}/webapi?/message"

        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "Cancel",
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

        return response

    def try_replace_invocation(self, body: dict, url) -> Response:
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "Replace",
            "id": random.randint(0, 10000),
            "params": body
        })
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response

    def invoke(self, body: dict, url: str):
        payload = json.dumps(body)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    def sign_invocation(self, correlation_id: str, signature: str, signer: str) -> Response:
        url = f"{self.server_url}/webapi?/message"

        body = {
            "jsonrpc": "2.0",
            "method": "Sign",
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
        return response

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
                    'public_key_str': signer['publicKey']
                }
        return result

    def load_connection_profile(self, profile: dict):
        url = f"{self.server_url}/webapi/configure/"

        payload = json.dumps(profile)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 204)

    def get_invocation_template(self) -> dict:
        private_key = self.signers["alice"]["privateKey"]
        public_key = self.signers["alice"]["public_key_str"]

        params = {
            "functionIdentifier": "",
            "inputs": [],
            "outputs": [],
            "timeout": 1000000,
            "doc": 0,
            "callbackUrl": config["BAL_CALLBACK_URL"],
            "signature": "",
            "proposer": "",
            "correlationIdentifier": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),

            "typeArguments": [],
            "signers": [],
            "minimumNumberOfSignatures": 0
        }

        signature = Ecdsa.sign(params["correlationIdentifier"], private_key)
        base64_encoded_signature = signature.toBase64()
        params["proposer"] = public_key
        params["signature"] = base64_encoded_signature

        return {
            "jsonrpc": "2.0",
            "method": "Invoke",
            "id": random.randint(0, 10000),
            "params": params
        }

    def start_plugin(self):
        url = f"{self.server_url}/webapi/plugins/{self.plugin}/start"

        payload = {}
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def get_proposer_signature(self, message) -> (str, str):
        private_key = self.signers["alice"]["privateKey"]
        public_key = self.signers["alice"]["public_key_str"]

        signature = Ecdsa.sign(message, private_key)
        base64_encoded_signature = signature.toBase64()
        return public_key, base64_encoded_signature
