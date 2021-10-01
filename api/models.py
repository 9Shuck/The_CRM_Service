from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy.sql.schema import Column
from werkzeug.security import check_password_hash

db = SQLAlchemy()

modifications = Table("modifications", db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("customer_id", ForeignKey("customer.id"), primary_key=True)
)

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'User {self.id}, {self.email}'
    
    def serialize(self):
        return {
            "id": self.id,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "email": self.email,
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
    
    def disable_user(self):
        self.is_active = False
        db.session.commit()

    @classmethod
    def get_all(cls):
        get_all = cls.query.all()
        return get_all

    @classmethod
    def get_by_email(cls, email):
        user = cls.query.filter_by(email=email).one_or_none()
        return user
    
    @classmethod
    def get_by_id(cls, id):
        user = cls.query.get(id)
        return user

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

class Customer(db.Model):

    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    photo_url = db.Column(db.String, nullable=False, default="https://via.placeholder.com/150")

    user_id = db.Column(db.Integer, ForeignKey('user.id'))

    def __repr__(self):
        return f'Customer {self.id}, {self.name}, {self.user_id}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "photo_url": self.photo_url,
            "user_id": self.user_id,
            "is_active": self.is_active
        }

    def create(self):
        db.session.add(self)
        db.session.commit()

    def disable_user(self):
        self.is_active = False
        db.session.commit()

    @classmethod
    def get_all(cls):
        get_all = cls.query.all()
        return get_all    
    
    @classmethod
    def get_by_id(cls, id):
        user = cls.query.get(id)
        return user

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self