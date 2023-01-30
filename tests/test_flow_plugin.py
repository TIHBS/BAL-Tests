import math
import unittest
import os
import json
import time
from tests.test_base import TestBase
import requests


class TestFlowPlugin(TestBase):
    def __init__(self, *args, **kwargs):
        super(TestFlowPlugin, self).__init__(*args, **kwargs)
        self.address = "0xf8d6e0586b0a20c7/Example"
        self.blockchain_id = "flow-1"

    def setUp(self):
        super(TestFlowPlugin, self).setUp()

        self.plugin_path = os.path.join("assets", "bal-generic-plugin-1.0-SNAPSHOT.jar")
        self.plugin = "generic-plugin"

        self.upload_plugin()
        self.start_plugin()

        connection_profile = {
            "flow-1": {
                "@type": "generic",
                "remotePluginUrl": "http://localhost:7878",
                "canHandleDelegatedSubscription": False
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

    def test_invoke_with_error(self):
        url = f"{self.server_url}/webapi?" \
              f"blockchain={self.plugin}" \
              f"&blockchain-id={self.blockchain_id}" \
              f"&address={self.address}"
        template = self.get_invocation_body_1()
        template["params"]["inputs"] = [
            {"name": "name", "type": "{\"type\":\"string\"}", "value": "test-2 NFT"},
            {"name": "newBooleanVar", "type": "{\"type\":\"boolean\"}", "value": "true"},
            {"name": "newInt8Var", "type": "{\"type\":\"integer\",\"maximum\": \"127\", \"minimum\": \"-1280\"}",
             "value": "-10"},
            {"name": "newUInt128Var",
             "type": "{\"type\":\"integer\",\"maximum\": \"340282366920938463463374607431768211455\", \"minimum\": \"0\"}",
             "value": "1000"}]

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
                "eventIdentifier": "StringUpdate",
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

    def test_query_with_filter(self):
        url = f"{self.server_url}/webapi?" \
              f"blockchain={self.plugin}" \
              f"&blockchain-id={self.blockchain_id}" \
              f"&address={self.address}"

        template = self.get_invocation_body_1()
        template["params"]["inputs"] = [
            {"name": "name", "type": "{\"type\":\"string\"}", "value": "test-2 NFT"},
            {"name": "newBooleanVar", "type": "{\"type\":\"boolean\"}", "value": "true"},
            {"name": "newInt8Var", "type": "{\"type\":\"integer\",\"maximum\": \"127\", \"minimum\": \"-128\"}",
             "value": "-10"},
            {"name": "newUInt128Var",
             "type": "{\"type\":\"integer\",\"maximum\": \"340282366920938463463374607431768211455\", \"minimum\": \"0\"}",
             "value": "1000"}]

        start_time = str(math.floor((time.time() - 100) * 1000))
        self.invoke(template, url)

        time.sleep(5)

        query_body = {
            "jsonrpc": "2.0",
            "method": "Query",
            "id": 29433,
            "params": {
                "eventIdentifier": "StringUpdate",
                "filter": "name==\"newValue\" and value==\"test-2 NFT\"",
                "typeArguments": [],
                "timeframe": {
                    "from": start_time,
                    "to": str(math.floor(time.time() * 1000))
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
        self.assertTrue(len(data['result']["occurrences"]) >= 1)

    def get_invocation_body_1(self) -> dict:
        template = self.get_invocation_template()
        template["params"]["functionIdentifier"] = "setValues"
        template["params"]["inputs"] = [
            {"name": "name", "type": "{\"type\":\"string\"}", "value": "test NFT"},
            {"name": "newBooleanVar", "type": "{\"type\":\"boolean\"}", "value": "true"},
            {"name": "newInt8Var", "type": "{\"type\":\"integer\",\"maximum\": \"127\", \"minimum\": \"-128\"}",
             "value": "-10"},
            {"name": "newUInt128Var",
             "type": "{\"type\":\"integer\",\"maximum\": \"340282366920938463463374607431768211455\", \"minimum\": \"0\"}",
             "value": "1000"}]
        return template


if __name__ == '__main__':
    unittest.main()
