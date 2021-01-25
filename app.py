from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

Base = automap_base()
engine = create_engine('mysql+pymysql://root:1@localhost:27017/avto')
Base.prepare(engine,reflect=True)
Avto = Base.classes.avto
Cities = Base.classes.cities
Session = sessionmaker(bind=engine)
session = Session()



app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)




# def connect_db():
# 	with engine.connect() as conn:
# 		return conn

@app.route('/')
def index():
	return render_template('index.html')

