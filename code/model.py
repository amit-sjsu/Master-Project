from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


#from flask_restless import APIManager

app = Flask(__name__)

DATABASE = 'drug_addict'
PASSWORD = 'password'
USER = 'root'
HOSTNAME = 'localhost'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate_obj = Migrate(app, db)
manager_obj = Manager(app)

manager_obj.add_command('db', MigrateCommand)


class CreateDB():
    def __init__(self):
        import sqlalchemy
        engine = sqlalchemy.create_engine('mysql://%s:%s@%s'%(USER, PASSWORD, HOSTNAME)) # connect to server
        engine.execute("CREATE DATABASE IF NOT EXISTS %s "%(DATABASE)) #create db


class Age(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.String(100))
    age_probability = db.Column(db.Float)
    age_drug_probability = db.Column(db.Float)


    def __init__(self, age, age_probability, age_drug_probability):
        self.age = age
        self.age_probability = age_probability
        self.age_drug_probability = age_drug_probability



if __name__ == '__main__':
	manager_obj.run()