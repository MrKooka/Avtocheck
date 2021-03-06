from flask import render_template,Blueprint,redirect,url_for,request,jsonify,current_app,flash
from flask_login import login_user,logout_user,current_user
#декоратор который скрывает обработчики от пользователей с неподходищими ролями
from flask_security import login_required
from werkzeug.security import generate_password_hash, check_password_hash


from .form import RequestForm_,RegisterForm_,LoginForm,LoginForm
from models import Cities,User,Role,RequestForm,Avto
from app import db,user_datastore
from logic import Logic


cars = Blueprint('cars', __name__, template_folder='templates')


@cars.route('/')
def index():
	# Поисковая строка
	q = request.args.get('q')
	if q:
		data = Avto.query.filter(Avto.name.contains(q)).all()
	else:
		data = Avto.query.all()

    # Пагинация 
	page = request.args.get('page')
	if page and page.isdigit():
		page = int(page)
	else:
		page = 1 
	pages = Avto.query.paginate(page=page,per_page = 9)
	return render_template('cars/index.html',data=data, pages=pages)

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

		try:

			
			data = RequestForm(phone=int(phone),name=name,email=email,city=city,
							   comment=comment,id_car=id_car)
			flash('Форма отпрвлена')
		except:
			flash('Не все поля формы заполнены корректно')
			return redirect(url_for('cars.choice_car',id_car=id_car))
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
	if form.validate_on_submit():

		if request.form['b'] == 'a':
			# try:
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
			# except:
			# 	print('Ошибка при доьавлении в базу ')
			# 	redirect(url_for('cars.signup'))
			return redirect(url_for('.index'))
		return redirect(url_for('cars.signup'))
		if request.form['b'] == 'b':
			try:
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
			except:
				redirect(url_for('cars.signup'))
			return redirect(url_for('.index'))
		return redirect(url_for('cars.signup'))
	return render_template('cars/signup.html',form=form)


@cars.route('/login',methods=['POST','GET'])
def login():
	print(current_user.__dict__)
	form = LoginForm()
	if form.validate_on_submit():
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
	l = Logic()
	role = [getattr(i,'discription') for i in current_user.roles][0]
	form_and_car_id = l.get_form_and_car_id()
	return render_template('cars/profil.html',role=role,current_user=current_user,Avto=Avto,\
							form_and_car_id=form_and_car_id,RequestForm=RequestForm,\
							)
	


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

# @cars.route('/signup', methods=['POST','GET'])
# def test():
# 	form = RegisterForm_()
# 	print(form.email.errors)
# 	# [print(i) for i in dir(form)]
# 	if form.validate_on_submit():
# 		request.form['b']


		
# 	else:
# 		print('Не POST')
# 	return render_template('cars/signup.html',form=form)