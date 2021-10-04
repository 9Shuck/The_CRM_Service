import unittest
import requests

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

class ApiTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/"
    USER_URL = "{}user".format(API_URL)
    LOGIN = "{}login".format(API_URL)

    def test_1_login(self):
        r = requests.post(ApiTest.LOGIN, json = {'email': 'admin@crm.com',
                                        'password': '123456aB'})
        self.assertEqual(r.status_code, 200)

    def test_2_get_all_users(self):
        r = requests.get(ApiTest.USER_URL, auth=BearerAuth('3pVzwec1Gs1m'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)


# if __name__ == '__main__':
#     unittest.main() 