from app import app
from models import Avto,RequestForm

class Logic:
	def __init__(self ,*args,**kwargs):
		pass

	def get_orders(self):
		orders = RequestForm.query.all()
		
		return orders
	
	def get_form_and_car_id(self):
		form_and_car_id = []
		for item in self.get_orders():
			form_and_car_id.append({'id_car':str(item.id_car),
									'id_form':str(item.id)})
		return form_and_car_id

	
if __name__ == '__main__':
	
	l = Logic()

	l.get_set_form_and_car()