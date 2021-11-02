from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from pool_project.models import User

class LoginForm(FlaskForm):
    email = StringField("Email",  validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField("Email",  validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', 
                                                                                            message='Field must be equal to Password field.')])
    terms = BooleanField('I agree to the terms of service and privacy policy.', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first(): #reusing login equery
            raise ValidationError('Email in User')

class ResetTokenForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Email')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', 
                                                                                            message='Field must be equal to Password field.')])
    submit = SubmitField('Reset Password')