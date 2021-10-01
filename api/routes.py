from flask import Blueprint, json, jsonify, request
from sqlalchemy import exc
from api.models import User, Customer
from api.validations import Validations
from api.errors import Errors
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import jwt
from datetime import timedelta

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def user_login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not (email and password):
        return Errors.missing_information()
    user = User.get_by_email(email)
    if user and check_password_hash(user.password, password) and user.is_active:
        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))
        return {'token': token}, 200
    return Errors.email_password()

@api.route('/register', methods=['POST'])
@jwt_required()
def user_register():
    if Validations.is_admin(get_jwt_identity()):
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if Validations.email(email):
            if Validations.password(password):
                user = User(
                    email = email,
                    password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
                )
                try: 
                    user.create()
                    return jsonify(user.serialize()), 201
                except exc.IntegrityError:
                    return Errors.email_already_registered()
            return Errors.password_not_valid()
        return Errors.email_not_valid()
    return Errors.not_admin()

@api.route('/user', methods=['GET'])
@jwt_required()
def get_all_users():
    if Validations.is_admin(get_jwt_identity()):
        all_users = User.get_all()
        if all_users:
            return jsonify([user.serialize() for user in all_users])
        return Errors.user_not_found()
    return Errors.not_admin()

@api.route('/customer', methods=['GET'])
@jwt_required()
def get_all_customers():
    all_customers = Customer.get_all()
    if all_customers:
        return jsonify([customer.serialize() for customer in all_customers])
    return Errors.customer_not_found()

@api.route('/customer/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    customer = Customer.get_by_id(id)
    if customer:
        return jsonify(customer.serialize())
    return Errors.customer_not_found()

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
    if Validations.customer_name(name) and Validations.customer_name(surname):
        try: 
            customer.create()
            return jsonify(customer.serialize()), 201
        except exc.IntegrityError:
            return {'error':'Something is wrong'}, 409
    return Errors.name_not_valid()

@api.route('/user/<int:id>', methods=['DELETE'])
@jwt_required
def delete_user(id):
    if Validations.is_admin(get_jwt_identity()):
        if Validations.is_active(id):
            user = User.get_by_id(id)
            if user:
                user.disable_user()
                return jsonify(user.serialize()), 200
            return Errors.user_not_found()    
        return Errors.user_not_found()
    return Errors.not_admin()