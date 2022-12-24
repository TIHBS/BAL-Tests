import json
import unittest
from typing import Any

import requests


class TestBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestBase, self).__init__(*args, **kwargs)

    def setUp(self):
        self.server_url = "http://localhost:9091"
        self.plugin_dir = "/home/ash/Softwares/apache-tomcat-8.5.84/plugins"

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
