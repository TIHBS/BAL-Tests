import string
import unittest
import os
import random
import json

from tests.test_base import TestBase
import requests
from ellipticcurve.ecdsa import Ecdsa


class TestSuiPlugin(TestBase):
    def __init__(self, *args, **kwargs):
        super(TestSuiPlugin, self).__init__(*args, **kwargs)
        self.address = "0x2/devnet_nft"
        self.blockchain_id = "sui-1"

    def setUp(self):
        super(TestSuiPlugin, self).setUp()

        self.plugin_path = os.path.join("assets", "bal-generic-plugin-1.0-SNAPSHOT.jar")
        self.plugin = "generic-plugin"

        self.upload_plugin()
        self.start_plugin()

        connection_profile = {
            "sui-1": {
                "@type": "generic",
                "remotePluginUrl": "http://localhost:8585",
            }
        }
        self.load_connection_profile(connection_profile)

    def test_invoke(self):
        url = f"{self.server_url}/webapi?" \
              f"blockchain={self.plugin}" \
              f"&blockchain-id={self.blockchain_id}" \
              f"&address={self.address}"
        template = self.get_invocation_body_1()
        payload = json.dumps(template)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIsNone(data.get("error"))
        self.assertEqual('OK', data.get("result"))

        self.get_pending_transactions()

    def test_query(self):
        url = f"{self.server_url}/webapi?" \
              f"blockchain={self.plugin}" \
              f"&blockchain-id={self.blockchain_id}" \
              f"&address={self.address}"

        query_body = {
            "jsonrpc": "2.0",
            "method": "Query",
            "id": 29433,
            "params": {
                "eventIdentifier": "0x2::devnet_nft::MintNFTEvent",
                "filter": "",
                "typeArguments": [],
                "timeframe": {
                    "from": "0",
                    "to": "16723413193760000"
                },
                "parameters": []
            }
        }

        payload = json.dumps(query_body)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIsNone(data.get("error"))
        self.assertIsNotNone(data)
        self.assertIsNotNone(data.get('id'))
        self.assertIsNotNone(data.get('result'))

    def get_invocation_body_1(self) -> dict:
        template = self.get_invocation_template()
        template["params"]["functionIdentifier"] = "mint"
        template["params"]["inputs"] = [
            {"name": "name", "type": "string", "value": "Example NFT"},
            {"name": "description", "type": "string", "value": "An NFT created for testing"},
            {"name": "ipfs", "type": "string",
             "value": "ipfs://<removed>"}]

        return template


if __name__ == '__main__':
    unittest.main()
