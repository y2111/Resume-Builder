from datetime import datetime
from resume import db,login_manager,app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import get_debug_queries



@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))



class UserModel(db.Model,UserMixin):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password =  db.Column(db.String(60),nullable=False)
    userdetails = db.relationship('userdetails',backref='details',lazy=True)
    education = db.relationship('education',backref='edu',lazy=True)
    experience = db.relationship('experience',backref='exp',lazy=True)
    projects = db.relationship('projects',backref='pro',lazy=True)
    publications = db.relationship('publications',backref='pub',lazy=True)
    skills = db.relationship('skills',backref='skill',lazy=True)
    links = db.relationship('links',backref='link',lazy=True)
    achievements = db.relationship('achievements',backref='ach',lazy=True)
  
    projects = db.relationship('projects',backref='pro',lazy=True)
    def __retr__(self):
        return  "User {}  Email {}  Image {}".format(self.username,self.email,self.image_file)
    
    def add_to_database(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_database(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()
    

class userdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    designation = db.Column(db.String(120),nullable=False)
    phoneno =  db.Column(db.String(15),nullable=False)
    profile = db.Column(db.Text,nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

 
 
class education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    degree=db.Column(db.String(100),nullable=False)
    major=db.Column(db.String(100),nullable=False)
    guided=db.Column(db.String(100),nullable=True)
    start = db.Column(db.Date,nullable=False,default=datetime.today())
    end = db.Column(db.Date,nullable=False,default=datetime.today())
    cgpa = db.Column(db.Integer,nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    
    def __retr__(self):
        return  "name {}  cgpa {}  user_id {}".format(self.name,self.cgpa,self.user_id)


class experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100),nullable=False)
    position = db.Column(db.String(100),nullable=False)
    startexp = db.Column(db.DateTime,nullable=False,default=datetime.today())
    endexp = db.Column(db.DateTime,nullable=False,default=datetime.today())
    content = db.Column(db.Text,nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __retr__(self):
        return  "company {}  position {}  user_id {}".format(self.company,self.position,self.user_id)



class projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.String(100),nullable=False)
    description = db.Column(db.Text,default=None)
    url = db.Column(db.String(100),default=None)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __retr__(self):
        return  "projectname {}    user_id {}".format(self.projectname,self.user_id)

class publications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publicationname = db.Column(db.String(100),nullable=True)
    guided=db.Column(db.String(100),nullable=True)
    description = db.Column(db.Text,default=None,nullable=True)
    published = db.Column(db.String(100),default=None,nullable=True)
    url = db.Column(db.String(100),default=None,nullable=True)

    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __retr__(self):
        return  "publication {}    user_id {}".format(self.publicationname,self.user_id)


class skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skillname = db.Column(db.String(100),nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

class links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    linkname = db.Column(db.String(100),nullable=False)
    url = db.Column(db.String(100),default=None)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)


class achievements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    achname = db.Column(db.String(100),nullable=False)
    achdesc = db.Column(db.Text,nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)




def init_db():
    db.create_all()


if __name__ == '__main__':
    init_db()