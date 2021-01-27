from app import session,Cities

def get_cities():
	data = session.query(Cities).all()
	return data

data = get_cities()
[print(i.city) for i in data]