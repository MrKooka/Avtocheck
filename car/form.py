from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField,IntegerField
from wtforms import TextAreaField,SelectField,SelectMultipleField,FormField
from wtforms.validators import InputRequired,Email,Length,DataRequired
from wtforms.fields.html5 import SearchField
import sys
sys.path.insert(0,'/media/alex/Data1/two/Avtocheck')
# from app import session,Cities

class RequestForm_(FlaskForm):
	email    = StringField("Email:",validators=[Email()])
	phone    = IntegerField('Телефон:')
	name     = StringField('Ваше имя:')
	cities   = SelectField('Ваш город',choices=[])
	comment  = TextAreaField('Комментарий')
	submit   = SubmitField("Отправить заявку")

# class RegistrationForm(FlaskForm):
# 	email = SubmitField('Email:',validators=[Email()])
# 	phone = IntegerField('Телефон:')
# 	name = StringField('Ваше имя:')
# 	psw = PasswordField()


class LoginForm(FlaskForm):
    username = StringField('Email', validators=[Email()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    submit   = SubmitField("Войти")

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])