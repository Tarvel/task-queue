from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, FileField, TextAreaField, MultipleFileField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo('password', message='Passwords do not match')])
    submit = SubmitField("Sign up")

    def validate_username(self, username):
            user = User.query.filter_by(username=username.data).first()
            if user:
                 raise ValidationError("Username has been chosen, use a different one")


    def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user:
                 raise ValidationError("Email exists, use a different one")
            


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")

#     def validate_username(self, username):
#             user = User.query.filter_by(username=username.data).first()
#             if user:
#                  raise ValidationError("Username has been chosen, use a different one")
            
        