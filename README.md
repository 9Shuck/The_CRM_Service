# The CRM Service 

### 📜 Description: 

The objective is to create a REST API to manage customer data for a small shop. It will work as the backend side for a CRM interface that is being developed by a different team.
<hr>

### ▶️ Run the project: 

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
Install the environment:
```
pipenv install
```
Go inside the environment:
```
pipenv shell
```
Run the application:
```
python3 app.py
```
Login with this credentials to access the API:

```
email: admin@crm.com
password: 123456aB
```
<hr>

### 📡 Endpoints:

<h4>Access for every user:</h4>
POST /login

<h4>Access just for admin user:</h4>
POST /user <br>
GET /user <br>
PATCH /user/id <br>
DELETE /user/id <br>

<h4>Access just for admin user or no admin user who created the customer:</h4>
POST /customer <br>
GET /customer <br>
GET /customer/id <br>
PATCH /customer/id <br>
DELETE /customer/id <br>

<hr>

### 🧩 UML Diagram:

<img height="300" width="280" src="https://i.imgur.com/UmkSGDb.png"/>

<hr>

### 🛠 Languages and Tools: 

<p align="left"> <a href="https://flask.palletsprojects.com/" target="_blank"> 
<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> 
<img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="40" height="40"/> </a>
<a href="https://git-scm.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> 

