from flask import Blueprint
from flask import render_template

from flask import request
from app import db
from flask import Blueprint
from flask import redirect
from flask import url_for

from flask_security import login_required
from app import engine

cars = Blueprint('cars', __name__, template_folder='templates')


@cars.route('/')
def index():
	with engine.connect():
		data = engine.execute('SELECT * FROM avto;').fetchall()

	return render_template('cars/index.html',data=data)

@cars.route('/choice_car/<id_car>')
def choice_car(id_car):
	with engine.connect():
		cities = engine.execute('SELECT * FROM cities')
		data = engine.execute(f'SELECT id, name FROM avto WHERE id LIKE {id_car}').fetchall()
		id = data[0][0]
		name=data[0][1]
	
	return render_template('cars/car_from.html',name=name,id=id,cities=cities)