from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a86d1cff6f8aec59f277386398c6f3c5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///docker.db'


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from dockerwebengine import routes