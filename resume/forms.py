from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError,Regexp
from resume.models import UserModel
from flask_login import current_user
from flask_wtf.file import FileAllowed,FileField

from wtforms.fields.datetime  import DateField
from flask_sqlalchemy import SQLAlchemy


class RegistrationForm(FlaskForm):
    username =  StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        users = UserModel.find_by_username(username.data)
        if users:
            raise ValidationError('Username used already')

    def validate_email(self,email):
        email = UserModel.find_by_email(email.data)
        if email:
            raise ValidationError('Email used already')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


#Personal details
class resumebuilder(FlaskForm):
    name= StringField("Name",validators=[DataRequired(),Length(min=5)])
    designation = StringField("Designation",validators=[DataRequired(),Length(min=3)])
    email = StringField("Email Id",validators=[Email(),DataRequired()])
    phoneno= StringField("Phone No",validators=[Regexp('^[0-9]*$'),DataRequired()])
    profile = TextAreaField("Description",validators=[Length(min=10)])
    submit = SubmitField("Create Resume")

#user Education

class useredu(FlaskForm):
    college = StringField("College",validators=[DataRequired(),Length(min=5)])
    degree=StringField("Degree",validators=[DataRequired(),Length(min=5)])
    major=StringField("Major",validators=[DataRequired(),Length(min=5)])
    guided = StringField("Guided By",validators=[DataRequired(),Length(min=3)])		
    start = DateField('Start Date', format='%Y-%m-%d',validators=[DataRequired()])
    end  = DateField('End Date', format='%Y-%m-%d',validators=[DataRequired()])
    
    def validate_end(form, field):
    	if field.data < form.start.data:
    		raise ValidationError("End date cannot be earlier than start date.")

    cgpa  = StringField("CGPA",validators=[DataRequired()])  
    submit = SubmitField("Add Education")


  #Work Experience
class userexp(FlaskForm):
    company = StringField("Company",
        validators=[DataRequired(),Length(min=5)])
    position = StringField("Position",
        validators=[DataRequired(),Length(min=5)])
    startexp = DateField('Start Date', format='%Y-%m-%d', 
         validators=[DataRequired()])
    endexp  = DateField('End Date', format='%Y-%m-%d', 
        validators=[DataRequired()])

    def validate_endexp(form, field):
    	if field.data < form.startexp.data:
    		raise ValidationError("End date cannot be earlier than start date.")

    content = TextAreaField("Description",
        validators=[DataRequired(),Length(min=15)])
    submit = SubmitField("Add Work Experience")
    
# Projects
class userpro(FlaskForm):
    projectname = StringField("Project Name",validators=[DataRequired(),Length(min=3)])
    		
    description = TextAreaField("Description",validators=[Length(min=10)])
    url = StringField("Project Url",validators=[Length(min=5)])
    submit = SubmitField("Add Projects")

#publlication

class userpub(FlaskForm):
    publicationname = StringField("Project Name",validators=[DataRequired(),Length(min=3)])
    guided = StringField("Guided By",validators=[DataRequired(),Length(min=3)])		
    description = TextAreaField("Description",validators=[Length(min=10)])
    url = StringField("Project Url",validators=[Length(min=5)])
    submit = SubmitField("Add Projects")

class usersk(FlaskForm):
    skillname = StringField("Skill Name",validators=[DataRequired(),Length(min=3)])
    
    submit = SubmitField("Add Another skill")

class userli(FlaskForm):
    linkname = StringField("Profile Link",validators=[DataRequired(),Length(min=3)])
    
    submit = SubmitField("Add Another link")


class achieve(FlaskForm):
    achname = StringField("Acheivement",validators=[DataRequired(),Length(min=3)])
    achdesc = TextAreaField("Description",validators=[Length(min=10)])

    
    submit = SubmitField("Add")



class account(FlaskForm):
    new_username = StringField("New Username",
        validators=[DataRequired(),Length(min=3,max=20)])
    new_email = StringField("New EmailId",
        validators=[Email(),DataRequired()])
  
    picture = FileField("Update Profile Picture",validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update Account')
    def validate_username(self,new_username):
        if new_username.data != current_user.username:
            username = UserModel.find_by_username(new_username.data)
            if username:
                raise ValidationError("Username Already present")
    def validate_email(self,new_email):
        if new_email != current_user.email:
            emailid = UserModel.find_by_email(new_email.data)
            if emailid:
                return ValidationError("Email Id used already")


