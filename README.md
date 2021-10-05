# The CRM Service 

### 📜 Description: 

The objective is to create a REST API to manage customer data for a small shop. It will work as the backend side for a CRM interface that is being developed by a different team. <br>
<br>
The API should be only accessible by a registered user by providing an authentication mechanism. <br>

A User (no Admin) can: <br>
  ▸ Create a new customer (with name, surname and photo). <br>
  ▸ List all customers. <br>
  ▸ Get full customer information. <br>
  ▸ Update an existing customer. <br>
  ▸ Delete an existing customer (soft delete). <br>
  <br>
 An Admin User can do the previous actions and manage users: <br>
  ▸ Create users. <br>
  ▸ List users. <br>
  ▸ Update users. <br>
  ▸ Delete users. <br>
  ▸ Change admin status. <br>
  <br>
  Every time a customer is modified by a user, the relationship between them is stored in an association table called 'modifications'.
<hr>

### ▶️ Run the project (Local): 

This project works with these minimum versions: <br>
Python version 3.9 <br> 
Flask 2.0 <br>
Flask-SQLAlchemy 2.5 <br> 
Flask-JWT-extended 4.3.0 <br>

Clone this repository:
```
git clone https://github.com/9Shuck/the_crm_service.git
```
Go inside the directory if you are not in:
```
cd the_crm_service
```
Run the app:
```
flask run
```

Login with this credentials to access the API:

```
email: admin@crm.com
password: 123456aB
```
### ▶️ Run the project (Deployment): 

This project is deployed the Heroku: <br>
https://the-crm-service.herokuapp.com/

<hr>

### 📡 Endpoints Access:

The API can be accessed with Postman/Insomnia. <br>
If the project is running locally: {URL} = http://127.0.0.1:5000 <br>
If the project is running in the deployment: {URL} = https://the-crm-service.herokuapp.com <br>

<h4>Access for every user:</h4>
POST: {URL} /login

<h4>Access just for admin user:</h4>
POST: {URL} /user <br>
GET: {URL} /user <br>
PATCH: {URL} /user/id <br>
DELETE: {URL} /user/id <br>

<h4>Access just for admin user or no admin user who created the customer:</h4>
POST: {URL} /customer <br>
GET: {URL} /customer <br>
GET: {URL} /customer/id <br>
PATCH: {URL} /customer/id <br>
DELETE: {URL} /customer/id <br>

<hr>

### 🎞 Example:
<hr>

### 🧪 Run Tests:

Go inside the directory if you are not in:
```
cd the_crm_service
```
Run the flask app:
```
flask run
```
Run the tests:
```
python3 tests/test_login.py
```
If all test are correct, this example message should be shown:
```
----------------------------------------------------------------------
Ran 6 tests in 0.064s

OK
```
<hr>

### 🧩 UML Diagram:

<img height="300" width="280" src="https://i.imgur.com/UmkSGDb.png"/>

<hr>

### 🛠 Languages and Tools: 

<p align="left"> <a href="https://flask.palletsprojects.com/" target="_blank"> 
<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> 
<img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="40" height="40"/> </a>
<a href="https://git-scm.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> 

