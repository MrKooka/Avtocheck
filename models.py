from app import db
from flask_security import UserMixin, RoleMixin

class Avto(db.Model):
	id           = db.Column(db.Integer(),primary_key=True)
	name         = db.Column(db.String(255))
	price        = db.Column(db.Integer())
	transmission = db.Column(db.String(255))
	drive_unit   = db.Column(db.String(255))
	engen        = db.Column(db.String(255))
	type_engen   = db.Column(db.String(255))
	url          = db.Column(db.Text())
	year         = db.Column(db.String(100))
	city         = db.Column(db.String(255))
	
	def __init__(self,*args,**kwargs):
		super(Avto,self).__init__(*args,**kwargs)
	def __repr__(self):
		return '<id:{} , name: {}>'.format(self.id,self.name)	

class Cities(db.Model):
	id   = db.Column(db.Integer(),primary_key=True)
	city = db.Column(db.String(100))
	url  = db.Column(db.Text())

	def __init__(self,*args,**kwargs):
		super(Cities,self).__init__(*args,**kwargs)

	def __repr__(self):
		return'<city:{},url:{}'.format(self.city,self.url)


class RequestForm(db.Model):
	id      = db.Column(db.Integer, primary_key=True)
	phone   = db.Column(db.Integer, unique=True)
	name    = db.Column(db.String(140))
	email   = db.Column(db.String(140))
	city    = db.Column(db.String(140))
	comment = db.Column(db.Text(140))
	id_car  = db.Column(db.Integer)

	def __init__(self, *args, **kwargs):
		super(RequestForm, self).__init__(*args, **kwargs)
	def __repr__(self):
		return '<Имя: {}, Телефон: {}, Email:{}, id машины:{} >'.format(self.name, self.phone,self.emai,self.id_car)



### FLASK SECURITY ###
roles_users = db.Table('Roles_users',
						db.Column('user_id',db.Integer(),db.ForeignKey('user.id')),
						db.Column('role_id',db.Integer(),db.ForeignKey('role.id'))
						)


class User(db.Model,UserMixin):
	id       = db.Column(db.Integer(),primary_key=True)
	email    = db.Column(db.String(100),unique=True)
	password = db.Column(db.String(255))
	username = db.Column(db.String(15))
	phone    = db.Column(db.String(100),unique=True)
	active   = db.Column(db.Boolean())
	roles    = db.relationship('Role',secondary=roles_users, backref=db.backref('users',lazy='dynamic')) 

class Role(db.Model,RoleMixin):
	id   = db.Column(db.Integer(),primary_key=True)
	name = db.Column(db.String(100))
	#Опись роли , для чего та или иная роль пользователя.
	discription = db.Column(db.String(255))




