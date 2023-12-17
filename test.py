
import unittest
import json
from server import forum_app
from web_users import UserHandler, ForumUser

class TestUserHandler(unittest.TestCase):
    def setUp(self):
        self.handler = UserHandler()

    def test_user_creation(self):
        # Testing the creation of a new user
        new_user = self.handler.create_user("exampleuser", "Example User")
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.username, "exampleuser")

    def test_moderator_creation(self):
        # Testing the creation of a new moderator
        new_moderator = self.handler.create_moderator("modexample", "Moderator Example")
        self.assertIsNotNone(new_moderator)
        self.assertEqual(new_moderator.username, "modexample")
        self.assertTrue(new_moderator.is_moderator)

    def test_user_auth(self):
        # Testing user authentication
        valid_user = self.handler.create_user("authuser", "Auth User")
        auth_status = self.handler.validate_user(valid_user.user_id, valid_user.key)
        self.assertTrue(auth_status)

        invalid_auth = self.handler.validate_user(valid_user.user_id, "incorrect_key")
        self.assertFalse(invalid_auth)
