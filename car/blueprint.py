from flask import Blueprint
from flask import render_template

from flask import request
from app import db,Avto,Cities,session,RequestForm
from flask import Blueprint
from flask import redirect
from flask import url_for

from flask_security import login_required
from app import engine

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

	cq = request.args.get('cq')

	
	if cq:
		cities = session.query(Cities).filter(Cities.city.contains(cq)).all()
		return render_template('cars/car_from.html',cities=cities,id_car=id_car)
	else:	
		with engine.connect():

			cities = engine.execute('SELECT * FROM cities')
			data = engine.execute(f'SELECT id, name FROM avto WHERE id LIKE {id_car}').fetchall()
			id = data[0][0]
			name=data[0][1]
		

		return render_template('cars/car_from.html',name=name,id=id,cities=cities,id_car=id_car)
	if request.method == 'POST':
		print(request.form['comment'])
		forma = session.add(RequestForm(phone=request.form['phone'],
										name=request.form['name'],
										email=request.form['email'],
										city=request.form['city'],
										comment=request.form['comment'],
										id_car=int(request.form['id_car'])))
		session.commit()
		return redirect(url_for('index'))