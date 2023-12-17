import unittest
import json
from server import forum_app
from web_users import MemberManager

class TestMemberManager(unittest.TestCase):
    def setUp(self):
        self.member_manager = MemberManager()

    def test_user_creation(self):
        # Testing the creation of a new user
        new_user = self.member_manager.register_member("exampleuser", "Example User")
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.nickname, "exampleuser")

    def test_moderator_creation(self):
        # Testing the creation of a new moderator
        new_moderator = self.member_manager.create_forum_moderator("modexample", "Moderator Example")
        self.assertIsNotNone(new_moderator)
        self.assertEqual(new_moderator.nickname, "modexample")
        self.assertTrue(new_moderator.moderator_status)

    def test_user_auth(self):
        # Testing user authentication
        valid_user = self.member_manager.register_member("authuser", "Auth User")
        auth_status = self.member_manager.validate_member(valid_user.member_id, valid_user.access_key)
        self.assertTrue(auth_status)

        invalid_auth = self.member_manager.validate_member(valid_user.member_id, "incorrect_key")
        self.assertFalse(invalid_auth)

if __name__ == '__main__':
    unittest.main()
