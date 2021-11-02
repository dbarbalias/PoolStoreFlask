from flask import Flask
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

from config import Config

app.config.from_object(Config)

db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)

