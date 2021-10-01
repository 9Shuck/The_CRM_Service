class Errors:

    def missing_information():
        return {'error': 'missing information'}, 400

    def email_not_valid():
        return {'error':'email not valid'}, 400

    def password_not_valid():
        return {'error':'password not valid'} , 400

    def email_password():
        return {'error':'email or password are incorrects'}, 400

    def name_not_valid():
        return {'error':'name nor valid'}, 400
    
    def surname_not_valid():
        return {'error':'surname not valid'}, 400

    def not_admin():
        return {'error':'You are not an admin'}, 401

    def not_auth():
        return {'error':'You are not authorized'}, 401

    def not_logged():
        return {'error':'You need to login'}, 401

    def user_not_found():
        return {'error': 'User not found'}, 404
    
    def customer_not_found():
        return {'error': 'Customer not found'}, 404

    def email_already_registered():
        return {'error':'this e-mail is already registered'}, 409
    
    

    

