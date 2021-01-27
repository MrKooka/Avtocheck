from flask import Blueprint,jsonify
from flask import render_template

from flask import request
from app import db,Avto,Cities,session,RequestForm_
from flask import Blueprint
from flask import redirect
from flask import url_for

from flask_security import login_required
from app import engine

from .form import RequestForm


cars = Blueprint('cars', __name__, template_folder='templates')


@cars.route('/')
def index():

	q = request.args.get('q')

	with engine.connect():
		if q:
			# data = engine.execute('SELECT * FROM avto;').fetchall()
			data = session.query(Avto).filter(Avto.name.contains(q)).all()
			# data = engine.execute(f'SELECT * FROM avto WHERE name like "{q}"').fetchall()
		else:
			data = engine.execute('SELECT * FROM avto;').fetchall()

	return render_template('cars/index.html',data=data)



@cars.route('/choice_car/<id_car>',methods=['POST','GET'])
def choice_car(id_car):
	form = RequestForm()
	
	if request.method=="POST":
		phone = form.phone.data
		name = form.name.data
		email = form.email.data
		city = form.cities.data
		comment = form.comment.data
		id_car = request.form['value_id_car']

		session.add(RequestForm_(phone=phone,name=name,email=email,city=city,comment=comment,id_car=id_car))
		session.commit()
		return redirect(url_for('cars.index'))
	
	data = session.query(Cities).all()
	form.cities.choices = [(i.city, i.city) for i in data]
	cities = session.query(Cities).all()
	id_car = session.query(Cities).filter(Cities.id==id_car).first().id	
	
	return render_template('cars/car_from.html',id_car=id_car,form=form,cities=cities)

@cars.route('choice_car/city/<name>')
def city(name):
	cities = session.query(Cities).filter(Cities.city.contains(name)).all()
	cityArray = []

	for city in cities:
		cityObj = {}
		cityObj['id'] = city.id
		cityObj['name'] = city.city
		cityArray.append(cityObj)
	return jsonify({'cities':cityArray})