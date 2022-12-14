
from flask import Flask
from flask_login import LoginManager
import pymysql 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt








conn="mysql+pymysql://y12:password@localhost/recruitment"
app =  Flask(__name__)

app.config['SECRET_KEY'] = '852' #Prevents XSS
app.config['SQLALCHEMY_DATABASE_URI'] = conn


db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  


def sql_debug(response):
    queries = list(get_debug_queries())
    query_str = ''
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        stmt = str(q.statement % q.parameters).replace('\n', '\n       ')
        query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(q.duration * 1000, 2))

    print('=' * 80)
    print(' SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    print('=' * 80)
    print(query_str.rstrip('\n'))
    print('=' * 80 + '\n')

    return response




from resume import routes