import unittest
import json
from server import forum_app  # Import the Flask app from server.py
from web_users import MemberManager  # Import the MemberManager from server.py

class TestMemberManager(unittest.TestCase):
    def setUp(self):
        self.app = forum_app.test_client()  # Create a test client for the Flask app
        self.member_manager = MemberManager()

    def test_user_creation(self):
        # Test user creation
        response = self.app.post('/member', json={'member_name': 'testuser'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['member_name'], 'testuser')

    def test_moderator_creation(self):
        # Test moderator creation
        response = self.app.post('/add_moderator',
                                headers={'Master-Key': 'admin_key'},
                                json={'member_name': 'newmod', 'full_name': 'New Mod'})
        self.assertEqual(response.status_code, 201)

    def test_user_auth(self):
        # Test user authentication
        valid_user = self.member_manager.register_member("authuser", "Auth User")
        response = self.app.get(f'/member/{valid_user.member_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['member_name'], 'authuser')

        # Add more test cases for user authentication here

class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        forum_app.testing = True  # Use the forum_app from server.py
        self.app = forum_app.test_client()
        self.user_manager = UserManager()

    def test_create_user_endpoint(self):
        # Test the create user endpoint
        response = self.app.post('/user', json={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'testuser')

    def test_create_moderator_endpoint(self):
        response = self.app.post('/create_moderator',
                                headers={'Admin-Key': 'admin_key'},
                                json={'username': 'newmod', 'real_name': 'New Mod'})
        self.assertEqual(response.status_code, 201)

    def test_post_creation_endpoint(self):
        # Test post creation
        post_data = {'msg': 'This is a test post'}
        response = self.app.post('/post', json=post_data)
        self.assertEqual(response.status_code, 200)

    def test_post_read_endpoint(self):
        # Test reading a post
        # Create a post then test reading that post
        response = self.app.get('/post/1')  # Assuming a post with ID 1
        self.assertEqual(response.status_code, 200)

    def test_post_delete_endpoint(self):
        # Create a post and get its ID and key
        post_data = {'msg': 'Test Post for Deletion'}
        create_response = self.app.post('/post', json=post_data)
        post_id = create_response.json['id']
        key = create_response.json['key']

        # Delete the post
        delete_url = f'/post/{post_id}/delete/{key}'
        response = self.app.delete(delete_url)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
