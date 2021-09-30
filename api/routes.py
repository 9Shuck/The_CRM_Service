from flask import Blueprint, json, jsonify, request
from sqlalchemy import exc
from api.models import User, Customer
from werkzeug.security import check_password_hash, generate_password_hash

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def user_register():
    is_admin = request.json.get('is_admin', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = User(
        is_admin = is_admin,
        email = email,
        password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    )

    try: 
        user.create()
        return jsonify(user.serialize()), 201
    except exc.IntegrityError:
        return {'error':'Something is wrong'}, 409

@api.route('/login', methods=['POST'])
def user_login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not (email and password):
        return {'error': 'Missing information'}, 401
    user = User.get_by_email(email)
    if user and user.password == password:
        return {'message':'login works'}, 200
    return {'message': 'email or password incorrects'}, 401

@api.route('/user', methods=['GET'])
def get_all_users():
    all_users = User.get_all()
    if all_users:
        return jsonify([user.serialize() for user in all_users])
    return jsonify({'message': 'No account created'}), 404

@api.route('/customer', methods=['GET'])
def get_all_customers():
    all_customers = Customer.get_all()
    if all_customers:
        return jsonify([customer.serialize() for customer in all_customers])
    return jsonify({'message': 'No customer created'}), 404


