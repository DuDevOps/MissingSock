import unittest

# add requests to test http call if process are running
import requests

import json

# explicitly add path 
import os, sys

os.chdir("..")
sys.path.insert(1,os.getcwd())

from MissingSockApi.MissingSockApi_main import home, get_all_users, get_user

class Test_MissingSockApi(unittest.TestCase):
    TEST_URL="http://127.0.0.1:5001"

    def test_home(self):
        json_return = json.loads(home())
        self.assertEqual(json_return["website"]["home"],"home message", "function test")

    def test_api_home(self):
        response = requests.get(f"{self.TEST_URL}/")
        json_response = json.loads(response.text)
        self.assertEqual(response.status_code, 200, "Status from api ")
        self.assertEqual(json_response["website"]["home"],"home message")

    def test_get_all_users(self):
        json_return = json.loads(get_all_users())
        self.assertIn('users',json_return)

    def test_api_users(self):
        response = requests.get(f"{self.TEST_URL}/users")
        self.assertIn('users',json.loads(response.text))
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        json_return = get_user(user_id="0007")

        self.assertIsInstance(json_return,str,"Receive JSON str")
        self.assertIn('0007', json_return,"Received data for user_id")

        json_loads = json.loads(json_return)
        self.assertIsInstance(json_loads, dict, "convert JSON str to DICT")
        self.assertIn('0007', {json_loads['users']['user_id']}, "Check user_id in json return")


if __name__ == '__main__':
    unittest.main()