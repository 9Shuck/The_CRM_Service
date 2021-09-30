from flask import Blueprint, json, jsonify, request
from sqlalchemy import exc
from api.models import User, Customer

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def user_register():
    is_admin = request.json.get('is_admin', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = User(
        is_admin=is_admin,
        email=email,
        password=password
    )

    try: 
        user.create()
        return jsonify(user.serialize()), 201
    except exc.IntegrityError:
        return {'error':'Something is wrong'}, 409

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


