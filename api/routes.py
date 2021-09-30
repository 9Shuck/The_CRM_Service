from flask import Blueprint, json, jsonify, request
from sqlalchemy import exc
from api.models import User, Customer
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import jwt
from datetime import timedelta

api = Blueprint('api', __name__)

class Validations:
    def is_admin():
        admin = User.get_by_id(get_jwt_identity())
        return admin.is_admin

@api.route('/register', methods=['POST'])
@jwt_required()
def user_register():

    if Validations.is_admin():

        email = request.json.get('email', None)
        password = request.json.get('password', None)

        user = User(
            email = email,
            password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        )
        try: 
            user.create()
            return jsonify(user.serialize()), 201
        except exc.IntegrityError:
            return {'error':'Something is wrong'}, 409
    else:
        return {'error':'You are not an admin'}

@api.route('/login', methods=['POST'])
def user_login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not (email and password):
        return {'error': 'Missing information'}, 401
    user = User.get_by_email(email)
    if user and check_password_hash(user.password, password) and user.is_active:
        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))
        return {'token': token}, 200
    return {'message': 'email or password incorrects'}, 401

@api.route('/user', methods=['GET'])
@jwt_required()
def get_all_users():
    if Validations.is_admin():
        all_users = User.get_all()
        if all_users:
            return jsonify([user.serialize() for user in all_users])
        return jsonify({'message': 'No account created'}), 404
    return jsonify({'message':'You are not an admin'}), 409

@api.route('/customer', methods=['GET'])
@jwt_required()
def get_all_customers():
    all_customers = Customer.get_all()
    if all_customers:
        return jsonify([customer.serialize() for customer in all_customers])
    return jsonify({'message': 'No customer created'}), 404

@api.route('/customer/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    customer = Customer.get_by_id(id)
    if customer:
        return jsonify(customer.serialize())
    return jsonify({'message': 'No customer created'}), 404

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
    if name and surname:
        try: 
            customer.create()
            return jsonify(customer.serialize()), 201
        except exc.IntegrityError:
            return {'error':'Something is wrong'}, 409
