import unittest
import requests

data_admin = {'email': 'admin@crm.com', 'password': '123456aB'}
data_user = {'email': 'test@test.com', 'password': '123456aB'}
data_customer = {'name': 'Testing', 'surname' : 'Testing'}

def get_token():
    r = requests.post("http://127.0.0.1:5000/login", json = data_admin)
    token = r.json()['token']
    return(token)

access_token = get_token()
header = {'Content-type': 'application/json', 'Authorization' : f'Bearer {access_token}'}

class ApiTest(unittest.TestCase):

    API_URL = "http://127.0.0.1:5000/"
    USER_URL = "{}user".format(API_URL)
    CUSTOMER_URL = "{}customer".format(API_URL)
    LOGIN = "{}login".format(API_URL)

    def test_0_login(self):
        r = requests.post(ApiTest.LOGIN, json = data_admin)
        self.assertEqual(r.status_code, 200)
        
    def test_1_get_all_users(self):
        r = requests.get(ApiTest.USER_URL, headers = header)
        self.assertEqual(r.status_code, 200)

    def test_3_post_customer(self):
        r = requests.post(ApiTest.CUSTOMER_URL, json = data_customer, headers = header)
        self.assertEqual(r.status_code, 201)

    # def test_4_delete_customer(self):
    #     r = requests.delete(ApiTest.CUSTOMER_URL + '/' + (str(id)), headers = header)
    #     print(r.json())
    #     self.assertEqual(r.status_codes, 200)

    def test_5_get_all_customers(self):
        r = requests.get(ApiTest.CUSTOMER_URL, headers = header)
        self.assertEqual(r.status_code, 200)


        
# if __name__ == '__main__':
#     unittest.main() 