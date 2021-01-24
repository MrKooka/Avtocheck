from app import engine,db

def index():
	engine.connect()
	print(engine.execute("select  * from avto where id like 1").fetchone())

index()
def ad_car():
	engine.connect()
	print(engine.execute("SELECT name FROM avto WHERE id LIKE 2").fetchone())
ad_car()