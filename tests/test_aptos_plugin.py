import unittest
import os
import json
from tests.test_base import TestBase
import requests
from ellipticcurve.ecdsa import Ecdsa


class TestAptosPlugin(TestBase):

    def __init__(self, *args, **kwargs):
        super(TestAptosPlugin, self).__init__(*args, **kwargs)
        self.address = "0x9f709239a4caf988527df46b7dca3797b740e408e48aa713e79a87fe85a53c4d/message"
        self.blockchain = "aptos"

    def setUp(self):
        super(TestAptosPlugin, self).setUp()
        self.plugin_path = os.path.join("assets", "bal-aptos-plugin-1.0-SNAPSHOT.jar")
        self.plugin = "aptos-plugin"

        self.upload_plugin()
        self.start_plugin()

        connection_profile = {
            "aptos-1": {
                "@type": "aptos",
                "nodeUrl": "http://localhost:8080/v1",
                "keyFile": "/home/ash/Desktop/git/bal/bal-aptos-plugin/src/main/resources/local_testnet.json"
            }
        }

        self.load_connection_profile(connection_profile)

    def test_send_single_transaction(self):
        url = f"{self.server_url}/webapi?blockchain={self.blockchain}&blockchain-id=aptos-1&address={self.address}"
        template = self.get_sample_invocation_template_1()

        response = self.invoke(template, url)
        self.assertEqual(response.status_code, 200)

        result = response.json()

        self.assertIsNone(result.get('error'))

        self.get_pending_transactions()

    def test_mint_nft_transaction(self):
        url = f"{self.server_url}/webapi?blockchain={self.blockchain}&blockchain-id=aptos-1&address=0x3/token"
        template = self.get_sample_template_mint_nft()

        response = self.invoke(template, url)
        self.assertEqual(response.status_code, 200)

        result = response.json()

        self.assertIsNone(result.get('error'))

        self.get_pending_transactions()

    def test_send_invocation_with_multiple_signers(self):
        pending_invocations_count_before = len(self.get_pending_transactions())

        url = f"{self.server_url}/webapi?blockchain={self.blockchain}&blockchain-id=aptos-1&address={self.address}"
        template = self.get_sample_invocation_template_1()
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

        url = f"{self.server_url}/webapi?blockchain={self.blockchain}&blockchain-id=aptos-1&address={self.address}"
        template = self.get_sample_invocation_template_1()
        template["params"]["signers"] = ["123", "345"]
        template["params"]["minimumNumberOfSignatures"] = 1

        response = self.invoke(template, url)

        self.assertEqual(response.status_code, 200)

        p = next(p for p in self.get_pending_transactions() if
                 p["correlationIdentifier"] == template["params"]["correlationIdentifier"])

        self.assertIsNotNone(p)

        pub_key, sig = self.get_proposer_signature(p["invocationHash"])

        try_cancel_result = self.try_cancel_invocation(p['correlationIdentifier'], sig, pub_key)
        self.assertEqual(200, try_cancel_result.status_code)

        body = try_cancel_result.json()

        self.assertIsNotNone(body.get("result"))
        self.assertEqual(True, body["result"])

        pending_invocations_after = len(self.get_pending_transactions())
        self.assertEqual(pending_invocations_after, pending_invocations_count_before)

    def test_try_replace_invocation(self):
        pending_invocations_initial_count = len(self.get_pending_transactions())

        url = f"{self.server_url}/webapi?blockchain={self.blockchain}&blockchain-id=aptos-1&address={self.address}"
        template = self.get_sample_invocation_template_1()
        template["params"]["signers"] = ["123", "345"]
        template["params"]["minimumNumberOfSignatures"] = 1

        response = self.invoke(template, url)

        pending_invocations_before = self.get_pending_transactions()
        self.assertEqual(pending_invocations_initial_count + 1, len(pending_invocations_before))

        p = next(p for p in pending_invocations_before if
                 p["correlationIdentifier"] == template["params"]["correlationIdentifier"])
        self.assertIsNotNone(p)

        self.assertEqual(response.status_code, 200)
        replace_template = template['params']
        replace_template['signer'] = "123"
        replace_template['minimumNumberOfSignatures'] = 2

        del replace_template["proposer"]

        pub_key, sig = self.get_proposer_signature(p["invocationHash"])

        replace_template["signature"] = sig
        replace_template["signer"] = pub_key

        try_replace_response = self.try_replace_invocation(replace_template, url)

        self.assertEqual(200, try_replace_response.status_code)

        try_replace_result = try_replace_response.json()
        self.assertIsNone(try_replace_result.get("error"))
        self.assertTrue(try_replace_result["result"])

        pending_invocations_after = self.get_pending_transactions()
        self.assertEqual(len(pending_invocations_after), len(pending_invocations_before))

        invocation = next((x for x in pending_invocations_after if
                           x['correlationIdentifier'] == replace_template['correlationIdentifier']),
                          None)

        self.assertIsNotNone(invocation)
        self.assertEqual(invocation['minimumNumberOfSignatures'], 2)
        return template

    def test_sign_invocation(self):
        pending_invocations_initial_count = len(self.get_pending_transactions())

        url = f"{self.server_url}/webapi?blockchain={self.blockchain}&blockchain-id=aptos-1&address={self.address}"
        template = self.get_sample_invocation_template_1()
        template["params"]["signers"] = [self.signers["bob"]['public_key_str']]
        template["params"]["minimumNumberOfSignatures"] = 1

        response = self.invoke(template, url)
        self.assertEqual(200, response.status_code)
        pending_invocations = self.get_pending_transactions()

        self.assertEqual(pending_invocations_initial_count + 1, len(pending_invocations))

        invocation = next((x for x in pending_invocations if
                           x['correlationIdentifier'] == template["params"]['correlationIdentifier']),
                          None)

        correlation_identifier = invocation["correlationIdentifier"]
        invocation_hash = invocation["invocationHash"]

        private_key = self.signers["bob"]["privateKey"]
        public_key = self.signers["bob"]["public_key_str"]

        signature = Ecdsa.sign(invocation_hash, private_key)
        base64_encoded_signature = signature.toBase64()

        response = self.sign_invocation(correlation_identifier, base64_encoded_signature, public_key)
        self.assertEqual(200, response.status_code)
        body = response.json()
        self.assertIsNone(body.get("error"))

        self.assertTrue(body["result"])

    def test_sign_invocation_when_charlie_is_not_in_signers_list(self):
        pending_invocations_initial_count = len(self.get_pending_transactions())

        url = f"{self.server_url}/webapi?blockchain={self.blockchain}&blockchain-id=aptos-1&address={self.address}"
        template = self.get_sample_invocation_template_1()
        template["params"]["signers"] = [self.signers["bob"]['public_key_str']]
        template["params"]["minimumNumberOfSignatures"] = 1

        response = self.invoke(template, url)
        self.assertEqual(200, response.status_code)
        pending_invocations = self.get_pending_transactions()

        self.assertEqual(pending_invocations_initial_count + 1, len(pending_invocations))

        invocation = next((x for x in pending_invocations if
                           x['correlationIdentifier'] == template["params"]['correlationIdentifier']),
                          None)

        correlation_identifier = invocation["correlationIdentifier"]
        invocation_hash = invocation["invocationHash"]

        private_key = self.signers["charlie"]["privateKey"]
        public_key = self.signers["charlie"]["public_key_str"]

        signature = Ecdsa.sign(invocation_hash, private_key)
        base64_encoded_signature = signature.toBase64()

        response = self.sign_invocation(correlation_identifier, base64_encoded_signature, public_key)
        self.assertEqual(200, response.status_code)
        body = response.json()
        self.assertIsNone(body.get("error"))

        self.assertFalse(body["result"])

    def get_sample_invocation_template_1(self):
        template = self.get_invocation_template()
        template["params"]["inputs"] = [
            {
                "name": "message",
                "type": "{\"type\":\"string\"}",
                "value": "0xA850fvertyb475bAB36455c59f0D2339B28d74b894e3D1"
            }
        ]
        template["params"]["functionIdentifier"] = "set_message"
        return template

    def get_sample_template_mint_nft(self):
        template = self.get_invocation_template()
        correlation_id = template["params"]["correlationIdentifier"]
        template["params"]["functionIdentifier"] = "create_collection_script"
        template["params"]["inputs"] = [
            {
                "name": "name",
                "type": "{\"type\":\"string\"}",
                "value": "test: " + correlation_id
            }, {
                "name": "description",
                "type": "{\"type\":\"string\"}",
                "value": "description: " + correlation_id
            }, {
                "name": "uri",
                "type": "{\"type\":\"string\"}",
                "value": "uri: " + correlation_id
            }, {
                "name": "supply",
                "type": "{\"type\": \"integer\", \"minimum\": \"0\", \"maximum\":\"18446744073709551615\"}",
                "value": "100"
            }, {
                "name": "mutate_setting",
                "type": "{\"type\": \"array\", \"items\": \"boolean\"}",
                "value": json.dumps([False, False, False])
            }
        ]
        return template


if __name__ == '__main__':
    unittest.main()
