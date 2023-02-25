import json

from config import config
from tests.test_base import TestBase
import os
from ellipticcurve.ecdsa import Ecdsa


class TestClient1(TestBase):
    def __init__(self, *args, **kwargs):
        super(TestClient1, self).__init__(*args, **kwargs)
        self.address = "0xf8d6e0586b0a20c7/Example"
        self.blockchain_id = "flow-1"
        self.bal_flow_plugin_url = config["BAL_FLOW_PLUGIN"]

    def setUp(self):
        super(TestClient1, self).setUp()

        self.plugin_path = os.path.join("assets", "bal-generic-plugin-1.0-SNAPSHOT.jar")
        self.plugin = "generic-plugin"

        self.upload_plugin()
        self.start_plugin()

        connection_profile = {
            "flow-1": {
                "@type": "generic",
                "remotePluginUrl": self.bal_flow_plugin_url,
                "canHandleDelegatedSubscription": False
            }
        }
        self.load_connection_profile(connection_profile)

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

    def test_initiate_invocation(self):
        pending_invocations_initial_count = len(self.get_pending_transactions())

        print(f"Pending invocations before initiating Invoke request: {pending_invocations_initial_count}")
        url = f"{self.server_url}/webapi?blockchain={self.plugin}&blockchain-id={self.blockchain_id}" \
              f"&address={self.address}"
        template = self.get_invocation_body_1()

        template["params"]["signers"] = [self.signers["bob"]['public_key_str']]
        template["params"]["minimumNumberOfSignatures"] = 1

        print(f"Invoke request url: [{url}]")
        print(f"Invoke request body:\n{template}")

        response = self.invoke(template, url)

        print(f"Invoke response code: [{response.status_code}]")
        print(f"Invoke response body:\n[{response.json()}]")

        self.assertEqual(200, response.status_code)
        pending_invocations = self.get_pending_transactions()

        print(f"Pending invocations after initiating Invoke request: {len(pending_invocations)}")
