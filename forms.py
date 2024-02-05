from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

class MessagesForm(FlaskForm):
    recipient_emails = StringField()
    phone = StringField()
    subject = StringField()
    message = StringField()
    submit = SubmitField()

#Create a Search Form
class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")

#create login form
class LoginForm(FlaskForm):
	name = StringField("Username", validators=[DataRequired()])
	email = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Log In")

#create a userform class
class UserForm(FlaskForm):
	name = StringField("Name :", validators=[DataRequired()])
	username = StringField("Username : ('Be Advice Use Your Email As Your Username')", validators=[DataRequired()])
	email = StringField("Email Address :", validators=[DataRequired()])
	about_author = TextAreaField("About Author : ")
	password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
	password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
	profile_pic = FileField("Profile Pic : ")
	submit = SubmitField("Submit")

#create a Password class
class PasswordForm(FlaskForm):
	email = StringField("what's your Email", validators=[DataRequired()])
	password_hash = PasswordField("what's your Password", validators=[DataRequired()])
	submit = SubmitField("Submit")

#create a form class
class NamerForm(FlaskForm):
	name = StringField("what's your name", validators=[DataRequired()])
	submit = SubmitField("Submit")