import json
import unittest

from config import config
from tests.test_base import TestBase
import os
from ellipticcurve.ecdsa import Ecdsa


class TestClient2(TestBase):
    def __init__(self, *args, **kwargs):
        super(TestClient2, self).__init__(*args, **kwargs)
        self.address = "0xf8d6e0586b0a20c7/Example"
        self.blockchain_id = "flow-1"
        self.bal_flow_plugin_url = config["BAL_FLOW_PLUGIN"]

    def setUp(self):
        super(TestClient2, self).setUp()

        self.plugin_path = os.path.join("assets", "bal-generic-plugin-1.0-SNAPSHOT.jar")
        self.plugin = "generic-plugin"

    def test_sign_invocation(self):
        pending_invocations = self.get_pending_transactions()
        invocation = pending_invocations[0]

        print(f"Signing pending invocation:\n{invocation}")

        correlation_identifier = invocation["correlationIdentifier"]
        invocation_hash = invocation["invocationHash"]

        private_key = self.signers["bob"]["privateKey"]
        public_key = self.signers["bob"]["public_key_str"]

        signature = Ecdsa.sign(invocation_hash, private_key)
        base64_encoded_signature = signature.toBase64()

        print(
            f"Signing invocation with correlation_identifier:[{correlation_identifier}] "
            f"using public_key:[{public_key}]")

        response = self.sign_invocation(correlation_identifier, base64_encoded_signature, public_key)

        print(f"Sign response code:\n[{response.status_code}]")
        print(f"Sign response body:\n[{response.json()}]")

        self.assertEqual(200, response.status_code)
        body = response.json()
        self.assertIsNone(body.get("error"))

        self.assertTrue(body["result"])


if __name__ == "__main__":
    unittest.main()
