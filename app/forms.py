from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,PasswordField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError,Length
from .models import User

class LoginForm(FlaskForm):
    username=StringField("Name",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    remember_me =BooleanField("Remember Me")
    submit=SubmitField("Log In")


class RegistrationForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    email=StringField("Email", validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    password2=PasswordField("Confirm Password", validators=[EqualTo('password')])
    submit=SubmitField("Register")

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username already exists")
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email Id Already Registered. Try different Email Id.")

class EditProfileForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    about_me=TextAreaField("About Me",validators=[Length(min=0,max=300)])
    submit=SubmitField("Save Changes")
    def __init__(self,original_username,*args,**kwargs):
        super(EditProfileForm,self).__init__(*args,**kwargs)
        self.original_username=original_username
    def validate_username(self,username):
        if(username.data != self.original_username ):
            user=User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError("Username already exists")

class EmptyForm(FlaskForm):
    submit=SubmitField('Submit')

class PostForm(FlaskForm):
    post=TextAreaField("Say Something",validators=[DataRequired(),Length(min=1,max=300)])
    submit=SubmitField("Submit")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


