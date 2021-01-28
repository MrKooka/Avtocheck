from app import db
from models import Avto
a = Avto(name='lol',price=1212,transmission='sda',drive_unit='sadasd',engen='sdas',type_engen='sadasd',url='asd',city='asd',year=123)
db.session.add(a)
db.session.commit()