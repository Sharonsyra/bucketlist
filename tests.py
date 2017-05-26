import unittest
import json

from run import app, db
from models import User, BucketList, Item


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app_context().push()
        self.client = app.test_client()

        db.create_all()

        # ... Tests for register ... #

    def test_register_password_length(self):
        """Test that register accepts only the recommended password length"""
        register = {'username': "sharon",
                    'email': "sharon@sharon.com",
                    'password': "sha"}
        response = self.client.post("/auth/register", data=json.dumps(register))
        self.assertEqual(response.status_code, 400)

    def test_register_username_format(self):
        """Test that register uses right username format"""
        register = {'username': "123sharon",
                    'email': "sharon@sharon.com",
                    'password': "sharz"}
        response = self.client.post("/auth/register", data=json.dumps(register))
        self.assertEqual(response.status_code, 400)

    def test_register_registers_user(self):
        """Test that register method registers a user successfully!"""
        register = {'username': "sharon",
                    'email': "sharon@sharon.com",
                    'password': "sharz"}
        response = self.client.post("/auth/register", data=json.dumps(register))
        self.assertEqual(response.status_code, 201)

    def test_register_duplicate_usernames(self):
        """Test that register method rejects duplicate usernames"""
        register = {'username': "sharon",
                    'email': "sharon@sharon.com",
                    'password': "sharz"}
        response = self.client.post("/auth/register", data=json.dumps(register))
        self.assertEqual(response.status_code, 409)

    # ... Tests for login ... #

    def test_login_wrong_credentials(self):
        """Test that login rejects wrong credentials!"""
        register = {'username': "wanja",
                    'password': "wanjira"}
        response = self.client.post("/auth/login", data=json.dumps(register))
        self.assertEqual(response.status_code, 401)

    def test_login_blank_credential(self):
        """Test that login rejects blank username or password"""
        register = {'username': "sharon",
                    'password': ""}
        response = self.client.post("/auth/login", data=json.dumps(register))
        self.assertEqual(response.status_code, 400)

    def test_login_logs_in_user(self):
        """Test that a user logs in successfully!"""
        register = {'username': "sharon",
                    'password': "sharz"}
        response = self.client.post("/auth/login", data=json.dumps(register))
        self.assertEqual(response.status_code, 200)

    # ... Tests bucketlist ... #

    def test_bucket_list_create(self):
        """Test that bucket list creates a bucket list"""
        bucketlist = {"name": "go sky-diving",
                      "items": "take a selfie",
                      "done": False
                      }
        response = self.client.post("/bucketlists/", data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 201)

    def test_bucket_list_duplicates(self):
        """Test that bucket list rejects duplicate bucketlists"""
        bucketlist = {"name": "go sky-diving",
                      "items": "take a selfie",
                      "done": False
                      }
        response = self.client.post("/bucketlists/", data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 409)

    def test_bucket_list_view_all(self):
        """Test that bucket list displays all bucket lists"""
        bucketlist = {"name": "go sky-diving",
                      "items": "take a selfie",
                      "done": False
                      }
        response = self.client.post("/bucketlists/", data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 200)

    def test_single_bucket_list_view_one(self):
        """Test that single bucket list displays a single bucket list"""
        bucketlist = {"name": "go sky-diving",
                      "items": "take a selfie",
                      "done": False
                      }
        response = self.client.post("/bucketlist/", data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 200)

    def test_single_bucket_list_update(self):
        """Test that single bucket list updates the bucket list"""
        bucketlist = {"name": "go water rafting",
                      "items": "take a selfie",
                      "done": False
                      }
        response = self.client.post("/bucketlists/<id>", data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 200)

    def test_single_bucket_list_delete(self):
        """Test that single bucket list deletes the bucket list"""
        bucketlist = {"name": "go sky-diving",
                      "items": "take a selfie",
                      "done": False
                      }
        response = self.client.post("/bucketlist/<id>", data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 204)

    # ... Tests items ... #

    def test_items_display_all(self):
        """Test items displays all items"""
        item = {"name": "take selfies",
                "done": False
                }
        response = self.client.post("/bucketlists/<id>/items/", data=json.dumps(item))
        self.assertEqual(response.status_code, 200)

    def test_items_create(self):
        """Test items creates new item"""
        item = {"name": "take selfies",
                "done": False
                }
        response = self.client.post("/bucketlists/<id>/items/", data=json.dumps(item))
        self.assertEqual(response.status_code, 201)

    def test_items_duplicates(self):
        """Test that items rejects duplicates"""
        item = {"name": "take selfies",
                "done": False
                }
        response = self.client.post("/bucketlists/", data=json.dumps(item))
        self.assertEqual(response.status_code, 409)

    def test_item_update(self):
        """Test that item updates item"""
        item = {"name": "take many selfies",
                "done": False
                }
        response = self.client.post("/bucketlists/<id>/items/<item_id>", data=json.dumps(item))
        self.assertEqual(response.status_code, 200)

    def test_item_delete(self):
        """Test that item deletes item"""
        item = {"name": "take selfies"}
        response = self.client.post("/bucketlists/<id>/items/<item_id>", data=json.dumps(item))
        self.assertEqual(response.status_code, 204)



if __name__ == '__main__':
    unittest.main()