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
                "remotePluginUrl": "http://localhost:8545",
            }
        }
        self.load_connection_profile(connection_profile)

    def test_invoke(self):
        url = f"{self.server_url}/webapi?" \
              f"blockchain={self.plugin}" \
              f"&blockchain-id={self.blockchain_id}" \
              f"&address={self.address}"
        template = self.get_invocation_template()
        payload = json.dumps(template)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIsNone(data.get("error"))
        self.get_pending_transactions()

    def get_invocation_body(self) -> dict:
        return {
            "functionIdentifier": "mint",
            "inputs": [
                {"name": "name", "type": "string", "value": "Example NFT"},
                {"name": "description", "type": "string", "value": "An NFT created for testing"},
                {"name": "ipfs", "type": "string",
                 "value": "ipfs://<removed>"}],
            "outputs": [],
            "timeout": 1000000,
            "doc": 50,
            "callbackUrl": "http://127.0.0.1:5010/",
            "signature": "",
            "proposer": "",
            "correlationIdentifier": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),

            "typeArguments": [],
            "signers": [],
            "minimumNumberOfSignatures": 0
        }


if __name__ == '__main__':
    unittest.main()
