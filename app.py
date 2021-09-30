from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

from api.models import db
from api.routes import api

import os
# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
# db = SQLAlchemy(app)
db.init_app(app)
# migrate = Migrate(app, db)

app.register_blueprint(api)

with app.app_context():
    db.create_all()

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
    