from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField,IntegerField
from wtforms import TextAreaField,SelectField,SelectMultipleField,FormField
from wtforms.validators import InputRequired,Email,Length,DataRequired
from wtforms.fields.html5 import SearchField
import sys
import phonenumbers
 
sys.path.insert(0,'/media/alex/Data1/two/Avtocheck')
# from app import session,Cities

class RequestForm_(FlaskForm):
	email = StringField("Email:",validators=[Email('Некорректный email')])
	phone = IntegerField('Телефон:')
	name = StringField('Ваше имя:')
	cities = SelectField('Ваш город',choices=[])
	comment = TextAreaField('Комментарий')
	submit = SubmitField("Отправить заявку")

class RegisterForm_(FlaskForm):
    email = StringField('Email:',validators=[Email('некорректный email')])
    phone = IntegerField('Телефон:')
    username = StringField('Ваше имя', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Пароль',validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Зарегистрироваться')
# class RegisterForm_(FlaskForm):
#     phone = IntegerField('Телефон',validators=[InputRequired(message='Поеле не заполнено')])
#     email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email')])
#     username = StringField('Ваше имя')
#     password = PasswordField('password', validators=[InputRequired(message='Поеле не заполнено'), Length(min=8, max=80)])
#     submit = SubmitField('Зарегистрироваться')

#     def validate_phone(form, field):
#         if 10 > len(field.data) > 12:
#             raise ValidationError('Invalid phone number.')
#         try:
#             input_number = phonenumbers.parse(field.data)
#             if not (phonenumbers.is_valid_number(input_number)):
#                 raise ValidationError('Invalid phone number.')
#         except:
#             input_number = phonenumbers.parse("+1"+field.data)
#             if not (phonenumbers.is_valid_number(input_number)):
#                 raise ValidationError('Invalid phone number.')
# class RegisterForm(FlaskForm):
#     email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
#     username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
#     password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(),Email()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    submit = SubmitField('Войти')