import unittest
import json

from run import app, db
from models import User, BucketList, Item

from tests import BaseTestCase

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app_context().push()
        self.client = app.test_client()

        db.session.close()
        db.drop_all()
        db.create_all()

        self.register_details = {
                    'username': "sharon",
                    'email': "sharon@sharon.com",
                    'password': "sharz"
                    }

        self.login_details = {
                    'username': "sharon",
                    'password': "sharz"
                    }

        self.bucketlist_details = {
                    "name": "go sky-diving",
                    "done": False
                    }

        self.item = {
                    "name": "take many selfies",
                    "done": False
                     }

        # ... Tests for register ... #

    def test_register_password_length(self):
        """Test that register accepts only the recommended password length"""
        register = {'username': "sharon",
                    'email': "sharon@sharon.com",
                    'password': "sha"}
        response = self.client.post("/api/v1.0/auth/register", data=json.dumps(register))
        self.assertEqual(response.status_code, 400)

    def test_register_username_format(self):
        """Test that register uses right username format"""
        register = {'username': "123sharon",
                    'email': "sharon@sharon.com",
                    'password': "sharz"}
        response = self.client.post("/api/v1.0/auth/register", data=json.dumps(register))
        self.assertEqual(response.status_code, 400)

    def test_create_user(self):
        """Test that register method registers a user successfully!"""
        register = {'username': "sharon",
                    'email': "sharon@sharon.com",
                    'password': "sharz"}
        response = self.client.post("/api/v1.0/auth/register", data=json.dumps(register))
        self.assertEqual(response.status_code, 201)

    def test_register_duplicate_usernames(self):
        """Test that register method rejects duplicate usernames"""
       
        register = {'username': "sharon",
                    'email': "sharon@sharon.com",
                    'password': "sharz"}
        response = self.client.post("/api/v1.0/auth/register", data=json.dumps(register))
        self.assertEqual(response.status_code, 201)

        register_duplicate = {'username': "sharon",
                    'email': "sharon@sharon.com",
                    'password': "sharz"}
        response = self.client.post("/api/v1.0/auth/register", data=json.dumps(register_duplicate))
        self.assertEqual(response.status_code, 409)

    # ... Tests for login ... #

    def test_login_wrong_credentials(self):
        """Test that login rejects wrong credentials!"""
        register = {
                    'username': "wanja",
                    'password': "wanjira"
                    }
        response = self.client.post("/api/v1.0/auth/login", data=json.dumps(register))
        self.assertEqual(response.status_code, 401)

    def test_login_blank_credential(self):
        """Test that login rejects blank username or password"""
        register = {'username': "sharon",
                    'password': ""}
        response = self.client.post("/api/v1.0/auth/login", data=json.dumps(register))
        self.assertEqual(response.status_code, 400)

    def test_login_logs_in_user(self):
        """Test that a user logs in successfully!"""
        register = {'username': "sharon",
                    'password': "sharz"}
        response = self.client.post("/api/v1.0/auth/login", data=json.dumps(register))
        self.assertEqual(response.status_code, 200)

    # ... Tests bucketlist ... #

    def test_create_bucketlist(self):
        """Test that bucket list creates a bucket list"""
        bucketlist = {"name": "go sky-diving",
                      "done": False
                      }
        response = self.client.post("/api/v1.0/bucketlists/", data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 201)

    def test_bucket_list_duplicates(self):
        """Test that bucket list rejects duplicate bucketlists"""
        bucketlist = {"name": "go sky-diving",
                      "done": False
                      }
        response = self.client.post("/api/v1.0/bucketlists/", data=json.dumps(bucketlist))
        # self.assertEqual(response.status_code, 201)

        bucketlist1 = {"name": "go sky-diving",
                      "done": False
                      }
        response = self.client.post("/api/v1.0/bucketlists/", data=json.dumps(bucketlist1))
        self.assertEqual(response.status_code, 409)

    def test_view_bucketlists(self):
        """Test that bucket list displays all bucket lists"""
        response = self.app.get("/api/v1.0/bucketlists/",
                                headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        output = output["bucketlists"]
        bucketlist1 = output[0]
        bucketlist2 = output[1]
        # Both bucket lists are displayed
        self.assertEqual(bucketlist1.get("title"), "Knowledge Goals")
        self.assertEqual(bucketlist2.get("title"), "Adventures")

    def test_view_bucketlist(self):
        """Test that single bucket list displays a single bucket list"""
        bucketlist = {"name": "go sky-diving",
                      "done": False
                      }
        response = self.client.get("/api/v1.0/bucketlist/", data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 200)

    def test_update_bucketlist(self):
        """Test that single bucket list updates the bucket list"""
        bucketlist = {"name": "go water rafting",
                      "done": False
                      }
        response = self.client.put("/api/v1.0/bucketlists/<id>", data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 200)

    def test_delete_bucketlist(self):
        """Test that single bucket list deletes the bucket list"""
        bucketlist = {"name": "go sky-diving",
                      "done": False
                      }
        response = self.client.delete("/api/v1.0/bucketlist/<id>", data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 204)

    # ... Tests items ... #

    def test_get_items(self):
        """Test items displays all items"""
        item = {"name": "take selfies",
                "done": False
                }
        response = self.client.get("/api/v1.0/bucketlists/<id>/items/", data=json.dumps(item))
        self.assertEqual(response.status_code, 200)

    def test_create_item(self):
        """Test items creates new item"""
        item = {"name": "take selfies",
                "done": False
                }
        response = self.client.post("/api/v1.0/bucketlists/<id>/items/", data=json.dumps(item))
        self.assertEqual(response.status_code, 201)

    def test_items_duplicates(self):
        """Test that items rejects duplicates"""
        item = {"name": "take selfies",
                "done": False
                }
        response = self.client.post("/api/v1.0/bucketlists/", data=json.dumps(item))
        self.assertEqual(response.status_code, 409)

    def test_update_item(self):
        """Test that item updates item"""
        item = {"name": "take many selfies",
                "done": False
                }
        response = self.client.put("/api/v1.0/bucketlists/<id>/items/<item_id>", data=json.dumps(item))
        self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        """Test that item deletes item"""
        item = {"name": "take selfies",
                "done": False
                }
        response = self.client.delete("/api/v1.0/bucketlists/<id>/items/<item_id>", data=json.dumps(item))
        self.assertEqual(response.status_code, 204)



if __name__ == '__main__':
    unittest.main()