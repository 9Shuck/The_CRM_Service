from api.models import User, Customer
from flask_jwt_extended import get_jwt_identity
import re

regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
regex_password = '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$'
regex_customer_name = "^(?=.*?[A-Za-z])[A-Za-z+]+$"

class Validations:
    def is_admin(id):
        admin = User.get_by_id(id)
        return admin.is_admin

    def is_active(id):
        admin = User.get_by_id(id)
        return admin.is_active

    def is_customer_active(id):
        customer = Customer.get_by_id(id)
        return customer.is_active

    def email(email):
        if(re.search(regex_email, email)):
            return True
        return False

    def password(password):
        if(re.search(regex_password, password)):
            return True
        return False

    def customer_name(name):
        if(re.search(regex_customer_name, name)):
            return True
        return False

    def customer_user(id, jwt_identity):
        customer = Customer.get_by_id(id)
        if customer.user_id == jwt_identity:
            return True
        return False






