import hvac
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from onboarding_main import *

import unittest

# data to connect to the vault
vault_addr = os.environ["VAULT_ADDR"]
vault_token = os.environ["VAULT_TOKEN"]
role_name = os.environ["ROLE"]


class TestOnboarding(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Test start")

    def setUp(self):
        # Connect to Vault
        self.root_client = hvac.Client(
            url=vault_addr,
            token=vault_token,
            namespace="root",
        )
        auth = self.root_client.is_authenticated()
        print("root autheticated? " + str(auth))

        self.cde_client = hvac.Client(
            url=vault_addr,
            namespace="cde",
        )
        self.resp = self.cde_client.auth.jwt.jwt_login(
            role=role_name,
            jwt=os.environ["CI_JOB_JWT"],
            path="gitlab",
        )
        self.cde_client = hvac.Client(
            url=vault_addr, namespace="cde", token=self.resp["auth"]["client_token"]
        )
        auth = self.cde_client.is_authenticated()
        print("cde autheticated? " + str(auth))

    def test_vault_connection(self):
        """
        Test Vault onboarding using ELB for NPE environment.
        Using mockfiles to simulate information from canvas app, LDAP, and snow api

            Returns:
                True - when onboarding successful
        """
        # code
        onboarding_status = func_main(
            self.root_client,
            self.cde_client,
            sender,
            email_password,
            email_template,
            self.resp["auth"]["client_token"],
            vault_addr,
        )
        self.assertTrue(onboarding_status, "Onboarding failed...")

    def tearDown(self):
        print("must remove token")

    @classmethod
    def tearDownClass(cls):
        print("Test end")


if __name__ == "__main__":
    unittest.main(argv=["TST"], exit=False)
