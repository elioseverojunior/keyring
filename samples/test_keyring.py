#!/usr/bin/env python3

import os
import unittest
from unittest import mock

import keyring.backend
import keyring.errors


class KeyringBackend(keyring.backend.KeyringBackend):
    """A Keyring which always outputs same password"""

    priority = 1

    def set_password(self, servicename, username, password):
        pass

    def get_password(self, servicename, username):
        return "password from TestKeyring"

    def delete_password(self, servicename, username):
        pass


@mock.patch.dict(os.environ, {"SERVICE_NAME": "system"}, clear=True)
@mock.patch.dict(os.environ, {"USERNAME": "test"}, clear=True)
@mock.patch.dict(os.environ, {"PASSWORD": "password from TestKeyring"},
                 clear=True)
class TestKeyring(unittest.TestCase):
    def test_keyring_backend(self):
        keyring.set_keyring(KeyringBackend())
        try:
            keyring.set_password(
                os.environ.get("SERVICE_NAME"),
                os.environ.get("USERNAME"),
                os.environ.get("PASSWORD"),
            )
            print("password stored successfully")
            self.assertEqual(
                keyring.get_password(
                    os.environ.get("SERVICE_NAME"), os.environ.get("USERNAME")
                ),
                os.environ.get("PASSWORD"),
                "Keyring password is correct",
            )
        except keyring.errors.PasswordSetError:
            print("failed to store password")
        finally:
            keyring.delete_password(
                os.environ.get("SERVICE_NAME"), os.environ.get("USERNAME")
            )

    def test_keyring_without_backend(self):
        try:
            keyring.get_keyring()
            keyring.set_password(
                os.environ.get("SERVICE_NAME"),
                os.environ.get("USERNAME"),
                os.environ.get("PASSWORD"),
            )
            self.assertEqual(
              keyring.get_password(
                os.environ.get("SERVICE_NAME"), os.environ.get("USERNAME")
              ),
              os.environ.get("PASSWORD"),
              "Keyring password is correct",
            )
        except keyring.errors.PasswordSetError:
            print("failed to store password")
        finally:
            keyring.delete_password(
                os.environ.get("SERVICE_NAME"), os.environ.get("USERNAME")
            )
