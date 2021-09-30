from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy.sql.schema import Column

db = SQLAlchemy()

modifications = Table("modifications", db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("customer_id", ForeignKey("customer.id"), primary_key=True)
)

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'User {self.id}, {self.email}, {self.is_active}'
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
        
    def create(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        get_all = cls.query.all()
        return get_all

class Customer(db.Model):

    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    photo_url = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, ForeignKey('user.id'))

    def __repr__(self):
        return f'Customer {self.id}, {self.name}, {self.user_id}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "photo_url": self.photo_url
        }

    @classmethod
    def get_all(cls):
        get_all = cls.query.all()
        return get_all    