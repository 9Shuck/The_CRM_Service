from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from api.models import db, User, Customer, modifications
from api.validations import Validations
from api.errors import Errors
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def user_login():

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not (email and password):
        return Errors.missing_information()

    user = User.get_by_email(email)

    if not (user 
            and check_password_hash(user.password, password) 
            and user.is_active):
        return Errors.email_password()

    token = create_access_token(identity=user.id, 
                                expires_delta=timedelta(hours=24))

    return {'token': token}, 200


@api.route('/user', methods=['POST'])
@jwt_required()
def user_register():

    if not Validations.is_admin(get_jwt_identity()):
        return Errors.not_admin()

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not Validations.email(email):
        return Errors.email_not_valid()
    
    if not Validations.password(password):
        return Errors.password_not_valid()
        
    user = User(
        email = email,
        password = generate_password_hash(password, 
                                          method='pbkdf2:sha256', 
                                          salt_length=16)
    )

    try: 
        user.create()
        return jsonify(user.serialize()), 201
    except exc.IntegrityError:
        return Errors.email_already_registered()


@api.route('/user', methods=['GET'])
@jwt_required()
def get_all_users():

    if not Validations.is_admin(get_jwt_identity()):
        return Errors.not_admin()
   
    all_users = User.get_all()

    if all_users:
        return jsonify([user.serialize() for user in all_users])
    return Errors.user_not_found()


@api.route('/user/<int:id>', methods=['PATCH'])
@jwt_required()
def update_user(id):

    if not Validations.is_admin(get_jwt_identity()): 
        return Errors.not_admin()

    update_user = {
                'email' : request.json.get('email', None),
                'password': request.json.get('password', None),
                'is_admin': request.json.get('is_admin', None)
    }
    
    if not (Validations.email(update_user['email'])):
            return Errors.email_not_valid()

    if not (Validations.password(update_user['password'])):
        return Errors.password_not_valid()

    password = generate_password_hash(update_user["password"], 
                                      method='pbkdf2:sha256', salt_length=16)
                                      
    update_user["password"] = password

    user = User.get_by_id(id)

    if not (user and Validations.is_active(id)):
        return Errors.user_not_found()

    try:
        updated_user = user.update(**{
                            key: value for key, value in update_user.items()
                            if value is not None
                        })
        return jsonify(updated_user.serialize()), 200
    except exc.IntegrityError:
        return Errors.email_already_registered()


@api.route('/user/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):

    if not Validations.is_admin(get_jwt_identity()):
        return Errors.not_admin()
  
    user = User.get_by_id(id)

    if not (user and Validations.is_active(id)):
        return Errors.user_not_found()

    user.disable_user()

    return jsonify(user.serialize()), 200


@api.route('/customer', methods=['POST'])
@jwt_required()
def post_customer():

    name = request.json.get('name', None)
    surname = request.json.get('surname', None)
    photo_url = request.json.get('photo_url', None)
    user_id = get_jwt_identity()

    customer = Customer(
        name = name,
        surname = surname,
        photo_url = photo_url,
        user_id = user_id
    )

    if not Validations.customer_name(name):
        return Errors.name_not_valid()

    if not Validations.customer_name(surname):
        return Errors.surname_not_valid()

    try: 
        customer.create()
        return jsonify(customer.serialize()), 201
    except exc.IntegrityError:
        return {'error':'Something is wrong'}, 409
    

@api.route('/customer', methods=['GET'])
@jwt_required()
def get_all_customers():

    all_customers = Customer.get_all_active()

    customer_serialization = [customer.serialize() for customer in all_customers]

    if not len(customer_serialization) > 0:
        return Errors.customer_not_found()
    return jsonify(customer_serialization)

     
@api.route('/customer/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):

    customer = Customer.get_by_id(id)

    if not (customer and Validations.is_customer_active(id)):
        return Errors.customer_not_found()
    return jsonify(customer.serialize())
    

@api.route('/customer/<int:id>', methods=['PATCH'])
@jwt_required()
def update_customer(id):

    if not (Validations.is_admin(get_jwt_identity()) 
            or Validations.customer_user(id, get_jwt_identity())):
        return Errors.not_auth()

    update_customer = {
                'name' : request.json.get('name', None),
                'surname': request.json.get('surname', None),
                'photo_url': request.json.get('photo_url', None)
    }

    customer = Customer.get_by_id(id)

    if not (customer and Validations.is_customer_active(id)):
        return Errors.customer_not_found()

    if not Validations.customer_name(update_customer['name']):
        return Errors.name_not_valid()

    if not Validations.customer_name(update_customer['surname']):
        return Errors.surname_not_valid()
    
    updated_customer = customer.update(**{
                        key: value for key, value in update_customer.items()
                        if value is not None
                    })
    
    try:
        modification = modifications.insert().values(user_id=get_jwt_identity(), 
                                                     customer_id=customer.id)
        db.session.execute(modification)
        db.session.commit()
    except exc.IntegrityError:
        pass
    return jsonify(updated_customer.serialize()), 200

        
@api.route('/customer/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):

    if not Validations.is_customer_active(id):
        return Errors.customer_not_found()

    if not (Validations.is_admin(get_jwt_identity()) 
            or Validations.customer_user(id, get_jwt_identity())):
        return Errors.not_admin()
    
    customer = Customer.get_by_id(id)
    
    if not customer:
        return Errors.customer_not_found()   

    customer.disable_user()
    return jsonify(customer.serialize()), 200
   






