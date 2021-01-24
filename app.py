from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:1@localhost:27017/avto')


app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)

# def connect_db():
# 	with engine.connect() as conn:
# 		return conn

@app.route('/')
def index():
	return render_template('index.html')

