from app import db

class RequestForm(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	phone = db.Column(db.Integer, unique=True)
	name = db.Column(db.String(140))
	email = db.Column(db.String(140))
	city = db.Column(db.String(140))
	comment = db.Column(db.Text(140))
	id_car = db.Column(db.Integer)

	def __init__(self, *args, **kwargs):
		super(RequestForm, self).__init__(*args, **kwargs)
	def __repr__(self):
		return '<Имя: {}, Телефон: {}, Email:{}, id машины:{} >'.format(self.name, self.phone,self.emai,self.id_car)