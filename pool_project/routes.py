from flask import render_template, request, url_for, session, redirect
from pool_project import app, bcrypt, mail, db
from pool_project.forms import LoginForm, RegistrationForm, ResetTokenForm, ResetPasswordForm
from pool_project.models import User, Inventory
from flask_mail import Message
from flask_login import current_user, login_user
from pool_project.utils import ConnectionObject

@app.route('/')
def index():
    session['Test'] = 'this is a session test' 
    print(session)
    
    print(request.remote_addr)#to get ip address
    print(request.user_agent.platform) #get machine
    print(request.user_agent.browser)
    print(request.user_agent.language)
    if request.args.get('open_cart'):
        open_cart = True
    else:
        open_cart = False
    vw_inv = ConnectionObject().get_inventory() #returns a tuple of values
    vw_columns = ['name', 'description', 'price', 'img_file', 'item_catg_id']
    vw_reformat = {}
    for i in vw_inv:
        vw_reformat[i[-1]] = dict(zip(vw_columns, i[:-1]))
    return render_template('index.html', inv=vw_reformat, open_cart=open_cart)

@app.route('/item/description/<item_id>')
def item_desc(item_id):
    inventory = Inventory.query.filter_by(inv_id=item_id).first()
    if inventory:
        return render_template('item_desc.html', inv=inventory, size=len(inventory.item_img.all()), inv_enum = enumerate(inventory.item_img.all()))
    else:
        return '4oh4'
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data):
            #login_user(user)#, remember=form.remember_me.data) future additions
            return redirect('index')
            
        else:
            return 'incorrect email or passwrod'
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        u = User(email=form.email.data, pass_hash = User.encrypt_password(form.password.data))
        db.session.add(u)
        db.session.commit()
        return f'success account created for {form.email.data}'
    return render_template('register.html', form=form)

@app.route('/reset_token', methods=['GET', 'POST'])
def reset_token():
    form = ResetTokenForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            with mail.connect() as conn:
                msg = Message('reset instructions', recipients=[form.email.data], sender=app.config['MAIL_USERNAME'])
                msg.body = url_for('reset_password', token=user.get_reset_token(), _external=True)
                conn.send(msg)
            return 'An email has been sent with instructions'
        else:
            return 'there is no account with that email. Please create an account to login'
    return render_template('reset_token.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    user = User.verify_reset_token(token)
    if form.validate_on_submit():
        if user:
            user.pass_hash = User.encrypt_password(form.password.data)
            db.session.commit()
            return 'password reset'
        else:
            return 'bad token'
    return render_template('reset_password.html', form=form)
