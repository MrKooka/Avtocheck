from flask import Blueprint,jsonify
from flask import render_template

from flask import request
# from app import db,Avto,Cities,session,RequestFormORM
from flask import Blueprint
from flask import redirect
from flask import url_for

from models import Avto,RequestForm,Cities 
#декоратор который скрывает обработчики от пользователей с неподходищими ролями
from flask_security import login_required
from app import db

from .form import RequestForm_,RegisterForm,LoginForm

cars = Blueprint('cars', __name__, template_folder='templates')


@cars.route('/')
def index():

	q = request.args.get('q')

	if q:
		# data = engine.execute('SELECT * FROM avto;').fetchall()
		data = Avto.query.filter(Avto.name.contains(q)).all()
		# data = engine.execute(f'SELECT * FROM avto WHERE name like "{q}"').fetchall()
	else:
		data = Avto.query.all()

	return render_template('cars/index.html',data=data)



@cars.route('/choice_car/<id_car>',methods=['POST','GET'])
def choice_car(id_car):
	form = RequestForm_()
	
	if request.method=="POST":
		phone = form.phone.data
		name = form.name.data
		email = form.email.data
		city = form.cities.data
		comment = form.comment.data
		id_car = request.form['value_id_car']
		data = RequestForm(phone=phone,name=name,email=email,city=city,comment=comment,id_car=id_car)
		db.session.add(data)
		db.session.commit()
		return redirect(url_for('cars.index'))
	
	data = Cities.query.all()
	form.cities.choices = [(i.city, i.city) for i in data]
	cities = Cities.query.all()
	id_car = Cities.query.filter(Cities.id==id_car).first().id	
	
	return render_template('cars/car_from.html',id_car=id_car,form=form,cities=cities)

# @cars.route('choice_car/city/<name>')
# def city(name):
# 	cities = session.query(Cities).filter(Cities.city.contains(name)).all()
# 	cityArray = []

# 	for city in cities:
# 		cityObj = {}
# 		cityObj['id'] = city.id
# 		cityObj['name'] = city.city
# 		cityArray.append(cityObj)
# 	return jsonify({'cities':cityArray})

@cars.route('/login')
def login():
	form = LoginForm()
	return render_template('cars/login.html',form=form)