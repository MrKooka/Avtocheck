from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_admin import Admin,AdminIndexView	
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore,Security,current_user
from flask_login import LoginManager
app = Flask(__name__)
app.config.from_object(Configuration)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)
#Base = automap_base()
#engine = create_engine('mysql+pymysql://root:1@localhost:27017/avto')
#Base.prepare(engine,reflect=True)

# Avto = Base.classes.avto
# Cities = Base.classes.cities
# RequestFormORM = Base.classes.request_form
#Session = sessionmaker(bind=engine)
#session = Session()


migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)


### ADMIN ###
from models import Avto,User,Role,db
# Сохраняем принцип DRY 
class AdminMixin:
	# метод поторый проверяет доступность обработчика к конкретному пользователю 
	# Когда мы обращаемся к конктретным обработчикам этот метод работает автоматом 
	def is_accessible(self):
		return current_user.has_role('admin')
	# метод который срабатывает ,  если вьюха не доступна текущему пользователю
	def inaccessible_callback(self, name,**kwarg):
		# security - blueprint от flask-security 
		# next - определяет ту ссылку куда пользователь направлялся , то есть определяет ту страницу , куда мы поподем если залогинимся 
		# если пользователь не вошел в профильл админа , редиректим его в форму авторизации 
		return redirect(url_for('security.login',next=request.url)) 


# ограничиваем доступ к таблицам базы данных в админке 
class AdminView(AdminMixin,ModelView):
	pass

#ограничиваем доступ к самой админке 
class HomeAdminView(AdminMixin,AdminIndexView):
	pass
	

admin = Admin(app,'FlaskApp',url='/',index_view = HomeAdminView(name='Home'))
# admin.add_view(ModelView(Avto,session)) - прошлая версия
admin.add_view(AdminView(Avto,db.session))


### Flask-security ###
user_datastore = SQLAlchemyUserDatastore(db,User,Role)
# Подключаем flask-security к приожению
security = Security(app,user_datastore)

@app.route('/')
def index():
	return render_template('index.html')

