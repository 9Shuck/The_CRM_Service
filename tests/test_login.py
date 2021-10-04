import unittest
import requests
import json

data = {'email': 'admin@crm.com', 'password': '123456aB'}

access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzMzM1OTg1MSwianRpIjoiYTZlNWZmMDktMWEwYS00N2ZlLTgwNDMtZTRmOGE1YWQ3YmJmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjMzMzU5ODUxLCJleHAiOjE2MzM0NDYyNTF9.32_UyALiSDZTWjHmxNhE_VmG1TB3rNX0t8scS2vWxAE'
header = {'Content-type': 'application/json', 'Authorization' : 'Bearer {access_token}'}

class ApiTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/"
    USER_URL = "{}user".format(API_URL)
    CUSTOMER_URL = "{}customer".format(API_URL)
    LOGIN = "{}login".format(API_URL)

    def test_0_login(self):
        r = requests.post(ApiTest.LOGIN, json = data)
        self.assertEqual(r.status_code, 200)
        # This get the token string
        print(r.json()['token'])
        
    def test_1_testing(self):
        r = requests.get(ApiTest.USER_URL, headers=header)
        print(r.json())
        self.assertEqual(r.status_code, 200)

    def test_2_get_all_users(self):
        r = requests.get(ApiTest.USER_URL, headers=header)
        print(r.json())
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

    def test_3_get_all_customers(self):
        r = requests.get(ApiTest.CUSTOMER_URL, headers=header)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

        
# if __name__ == '__main__':
#     unittest.main() 