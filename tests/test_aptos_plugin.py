import string
import unittest
import os
import random
import json
from tests.test_base import TestBase
import requests


class TestAptosPlugin(TestBase):

    def __init__(self, *args, **kwargs):
        super(TestAptosPlugin, self).__init__(*args, **kwargs)
        self.plugin_path = os.path.join("assets", "bal-aptos-plugin-1.0-SNAPSHOT.jar")
        self.address = "9f709239a4caf988527df46b7dca3797b740e408e48aa713e79a87fe85a53c4d"
        self.blockchain = "aptos"

    def setUp(self):
        super(TestAptosPlugin, self).setUp()
        # self.upload_plugin()

        connection_profile = {
            "aptos-1": {
                "@type": "aptos",
                "nodeUrl": "http://localhost:8080/v1",
                "keyFile": os.path.join("assets", "aptos.json")
            }
        }
        # self.upload_connection_profile(body=connection_profile)

    def test_send_single_transaction(self):
        url = f"{self.server_url}/webapi?blockchain={self.blockchain}&blockchain-id=aptos-1&address={self.address}/message"
        template = self.get_invocation_tempate()
        payload = json.dumps(template)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)

        self.get_pending_transactions()

    def test_send_invocation_with_multiple_signers(self):
        pending_invocations_count_before = len(self.get_pending_transactions())

        url = f"{self.server_url}/webapi?blockchain={self.blockchain}&blockchain-id=aptos-1&address={self.address}/message"
        template = self.get_invocation_tempate()
        template["params"]["signers"] = ["123", "345"]
        template["params"]["minimumNumberOfSignatures"] = 1

        payload = json.dumps(template)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)

        pending_invocations = self.get_pending_transactions()
        self.assertIsNotNone(pending_invocations)
        self.assertEqual(len(pending_invocations), pending_invocations_count_before + 1)

    def test_cancel_invocation_with_multiple_signers(self):
        pending_invocations_count_before = len(self.get_pending_transactions())

        url = f"{self.server_url}/webapi?blockchain={self.blockchain}&blockchain-id=aptos-1&address={self.address}/message"
        template = self.get_invocation_tempate()
        template["params"]["signers"] = ["123", "345"]
        template["params"]["minimumNumberOfSignatures"] = 1

        payload = json.dumps(template)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)

        try_cancel_result = self.try_cancel_invocation(template['params']['correlationIdentifier'], "", "")
        self.assertTrue(try_cancel_result)

        pending_invocations_after = len(self.get_pending_transactions())
        self.assertEqual(pending_invocations_after, pending_invocations_count_before)

    def get_invocation_tempate(self) -> dict:
        return {
            "jsonrpc": "2.0",
            "method": "Invoke",
            "id": random.randint(0, 10000),
            "params": {
                "functionIdentifier": "set_message",
                "inputs": [
                    {
                        "name": "message",
                        "type": "{\"type\":\"string\"}",
                        "value": "0xA850fvertyb475bAB36455c59f0D2339B28d74b894e3D1"
                    }
                ],
                "outputs": [],
                "timeout": 1000000,
                "doc": 50,
                "callbackUrl": "http://127.0.0.1:5010/",
                "signature": "",
                "correlationIdentifier": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),

                "typeArguments": [],
                "signers": [],
                "minimumNumberOfSignatures": 0
            }
        }


if __name__ == '__main__':
    unittest.main()
