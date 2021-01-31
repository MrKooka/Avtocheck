from flask import render_template,Blueprint,redirect,url_for,request,jsonify,current_app
from models import Avto,RequestForm,Cities,User,Role
#декоратор который скрывает обработчики от пользователей с неподходищими ролями
from flask_security import login_required
from app import db,user_datastore
from .form import RequestForm_,RegisterForm_,LoginForm,LoginForm
from flask_login import login_user,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
cars = Blueprint('cars', __name__, template_folder='templates')


@cars.route('/')
def index():
	q = request.args.get('q')
	if q:
		data = Avto.query.filter(Avto.name.contains(q)).all()
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

@cars.route('/signup', methods=['POST','GET'])
def signup():
	form = RegisterForm_()
	print(request.form)
	if request.method=='POST':
		if request.form['b'] == 'a':
			hashed_pass = generate_password_hash(form.password.data,method='sha256')
			new_user = user_datastore.create_user(email=form.email.data,
												  password=hashed_pass,
												  phone=form.phone.data,
												  username=form.username.data)
			role = Role(name=form.username.data,discription='checkman')
			db.session.add(new_user)
			db.session.add(role)
			db.session.commit()
			user_datastore.add_role_to_user(new_user,role)
			db.session.commit()
			return redirect(url_for('.index'))
		if request.form['b'] == 'b':
			hashed_pass = generate_password_hash(form.password.data,method='sha256')
			new_user = user_datastore.create_user(email=form.email.data,
												  password=hashed_pass,
												  phone=int(form.phone.data),
												  username=form.username.data)
			role = Role(name=form.username.data,discription='user')
			db.session.add(new_user)
			db.session.add(role)
			db.session.commit()
			user_datastore.add_role_to_user(new_user,role)
			db.session.commit()
			return redirect(url_for('.index'))

	return render_template('cars/signup.html',form=form)
@cars.route('/login',methods=['POST','GET'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data)
				return redirect(url_for('cars.profil'))
		return '<h1>Invalid username or password</h1>'
	return render_template('cars/login.html',form=form)

@cars.route('/profil')
@login_required
def profil():
	role = [(i.__dict__)['discription'] for i in current_user.roles][0]
	name = current_user.username
	print(name)
	return render_template('cars/profil.html',role=role,name=name)

@cars.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

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

