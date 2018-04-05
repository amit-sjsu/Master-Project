from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


#from flask_restless import APIManager

app = Flask(__name__)

DATABASE = 'drug_addict_master_data'
PASSWORD = 'analyticsmypassabuse'
USER = 'analytics'
HOSTNAME = 'analyticsdb.cwmpirdjxqbj.us-east-1.rds.amazonaws.com'


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
    state = db.Column(db.String(100))


    def __init__(self, age, age_probability, age_drug_probability, state):
        self.age = age
        self.age_probability = age_probability
        self.age_drug_probability = age_drug_probability
        self.state = state


class Sex(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.String(100))
    sex_probability = db.Column(db.Float)
    sex_drug_probability = db.Column(db.Float)
    state = db.Column(db.String(100))


    def __init__(self, sex, sex_probability, sex_drug_probability, state):
        self.sex = sex
        self.sex_probability = sex_probability
        self.sex_drug_probability = sex_drug_probability
        self.state = state



class Race(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    race = db.Column(db.String(100))
    race_probability = db.Column(db.Float)
    race_drug_probability = db.Column(db.Float)
    state = db.Column(db.String(100))

    def __init__(self, race, race_probability, race_drug_probability, state):
        self.race = race
        self.race_probability = race_probability
        self.race_drug_probability = race_drug_probability
        self.state = state


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100))
    drug_count = db.Column(db.Float)
    census_count = db.Column(db.Float)

    def __init__(self, state, drug_count, census_count):
        self.state = state
        self.drug_count = drug_count
        self.census_count = census_count



if __name__ == '__main__':
	manager_obj.run()



