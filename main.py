from app import app
from car.blueprint import cars
# from admin.admin import admin
import views

app.register_blueprint(cars, url_prefix='/cars')
# app.register_blueprint(admin,url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)