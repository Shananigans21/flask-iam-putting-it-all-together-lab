from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from sqlalchemy import MetaData

app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})
db = SQLAlchemy(metadata=metadata)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
api = Api(app)
