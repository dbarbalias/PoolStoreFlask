import os
from pool_project import app 
from datetime import timedelta
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xa2\t\x0c\xc6\xd3\x02=G1Q\xf9O\xc3\x1fQ+'
    SERVER_LOCACTION = os.environ.get('SERVER_LOCATION') or  os.path.join(os.path.dirname(app.instance_path), 'app.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SERVER_LOCACTION 
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '' #removed
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '' #removed
    PERMANENT_SESSION_LIFETIME = timedelta(days=365)
