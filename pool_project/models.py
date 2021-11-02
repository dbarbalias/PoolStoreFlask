from pool_project import db, bcrypt, app, login
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as JWSS
from flask_login import UserMixin
from six import text_type #this is unicode
from sqlalchemy import CheckConstraint

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    pass_hash = db.Column(db.String(128), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    updt_date = db.Column(db.DateTime, default=datetime.utcnow) #tracks logins
    pool_id = db.Column(db.Integer)
    addr  = db.Column(db.String(128)) #https://endswithsaurus.wordpress.com/2009/07/23/a-lesson-in-address-storage/
    city = db.Column(db.String(50))
    zip_code = db.Column(db.Integer)
    state = db.Column(db.String(2))
    active = db.Column(db.Integer, nullable=False, default=0)

    def get_id(self): #overriding get_id
        try:
            return text_type(self.user_id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')
    @staticmethod
    def encrypt_password(password): #input is the form.password.data
        return bcrypt.generate_password_hash(password).decode('utf-8')
    def check_password(self, password): #input is the form.password.data
        return bcrypt.check_password_hash(self.pass_hash, password)

    def get_reset_token(self, expires_sec=1800):
        s = JWSS(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = JWSS(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Inventory(db.Model):
    inv_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(480))
    price = db.Column(db.Float(precision=2), nullable=False) 
    quantity = db.Column(db.Integer, nullable=False)
    item_catg_id = db.Column(db.Integer, nullable=False)

    item_rules = db.relationship('item_catg_rules', backref='inventory_tbl', lazy='dynamic') #backref naming should point to inventory
    item_img = db.relationship('item_img_path', backref='inv_tbl', lazy='dynamic') #backref naming should point to inventory

    CheckConstraint('price > 0', name='check_price')
    CheckConstraint('quantity >= 0', name='check_quantity')
    CheckConstraint('item_catg_id > 1', name='check_item_catg')

class item_catg_rules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_catg_id = db.Column(db.Integer, db.ForeignKey('inventory.item_catg_id')) #potential pk
    item_catg_desc = db.Column(db.String(480))

    CheckConstraint('item_catg_id > 1', name='check_item_catg')

class item_img_path(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inv_id = db.Column(db.Integer, db.ForeignKey('inventory.inv_id'))
    img_file = db.Column(db.String(480), nullable=False, default='default.png')
    img_catg = db.Column(db.Integer, nullable=False)

    CheckConstraint('img_catg >= 0', name='check_img_catg')




"""
class Sessions(db.Model): #table will be used to create carts for users
    session = #session id can be linked to the email if they login
    cart = db.Column(db.String(256) #this is the js obj of the cart associated with the session also stored in local storage
    user_id = #a constraint to link the 
"""
