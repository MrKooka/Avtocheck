from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField,IntegerField
from wtforms import TextAreaField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired,Email,Length
from wtforms.fields.html5 import SearchField
import sys
sys.path.insert(0,'/media/alex/Data1/two/Avtocheck')
from app import session,Cities

class RequestForm(FlaskForm):
	email = StringField("Email:",validators=[Email()])
	phone = IntegerField('Телефон:')
	name = StringField('Ваше имя:')
	cities = SelectField('Ваш город',choices=[])
	comment = TextAreaField('Комментарий')
	submit = SubmitField("Отправить заявку")
