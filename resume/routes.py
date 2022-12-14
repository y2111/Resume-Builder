from flask import Flask, render_template, url_for, flash, redirect,request,abort,make_response
from resume.forms import RegistrationForm, LoginForm,resumebuilder,useredu,userexp,userpro,usersk,achieve,userli,userpub,account
from resume import app,db,bcrypt
from resume.models import UserModel,userdetails,education,experience,projects,skills,achievements,publications,links
import secrets,os
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import pdfkit
from flask_sqlalchemy import SQLAlchemy




@app.route("/")
def page():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'),code=301)
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        username=form.username.data, email=form.email.data, password=hashed_password
        user = UserModel(username=form.username.data, email=form.email.data, password=hashed_password)
        
        db.session.add(user)
        connection = db.session.connection()
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'),code=301)
    form = LoginForm()
    if form.validate_on_submit():
        logged = UserModel.find_by_email(form.email.data)
        if logged and bcrypt.check_password_hash(logged.password,form.password.data):
           login_user(logged,remember=form.remember.data)
           return redirect(url_for('home'),code=301)
            
        else:
            flash('Login unsuccessful')

    return render_template('login.html',title='Login',form=form)




@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"),code=302)


@app.route("/resume/new",methods=['GET','POST'])
@login_required
def  post():
    form = resumebuilder()
    if form.validate_on_submit():
        usr = userdetails(name=form.name.data,email=form.email.data,designation=form.designation.data,phoneno=form.phoneno.data,profile=form.profile.data,details=current_user)
        db.session.add(usr)
        db.session.commit()
        print(form.name.data,form.email.data,form.designation.data)
        return redirect(url_for("postedu"),code=301)
    return render_template("usr.html",title="New Resume",form=form)


@app.route("/resume/new/education",methods=['GET','POST'])
@login_required
def  postedu():
    form = useredu()
    eduadded = education.query.filter_by(edu=current_user).all()
    print(str(eduadded))
    if form.validate_on_submit():
        edu = education(name=form.college.data,degree=form.degree.data,major=form.major.data,guided=form.guided.data,start=form.start.data,end=form.end.data,cgpa=form.cgpa.data,edu=current_user)
        print(form.college.data,form.start.data,form.end.data)
        db.session.add(edu)
        
        db.session.commit()
        #print(form.company.data,form.position.data)
        return redirect(url_for("postedu"),code=301)
    return render_template("education.html",title="Education",form=form,eduadded=eduadded)

@app.route("/resume/new/experience",methods=['GET','POST'])
@login_required
def  postexperience():
    form = userexp()
    expadded = experience.query.filter_by(exp=current_user).all()
    if form.validate_on_submit():
        exp = experience(company=form.company.data,position=form.position.data,startexp=form.startexp.data,endexp=form.endexp.data,content=form.content.data,exp=current_user)
        db.session.add(exp)
        db.session.commit()
        return redirect(url_for("postexperience"),code=301)
    return render_template("experience.html",title="Experience",form=form,expadded=expadded)


@app.route("/resume/new/projects",methods=['GET','POST'])
@login_required
def  postprojects():
    form = userpro()
    proadded = projects.query.filter_by(pro=current_user).all()
    if form.validate_on_submit():
        pro = projects(projectname=form.projectname.data,description=form.description.data,url=form.url.data,pro=current_user)
        db.session.add(pro)
        db.session.commit()
        return redirect(url_for("postpublications"),code=301)
    return render_template("projects.html",title="Projects",form=form,proadded=proadded)

@app.route("/resume/new/publications",methods=['GET','POST'])
@login_required
def  postpublications():
    form = userpub()
    pubadded = publications.query.filter_by(pub=current_user).all()
    if form.validate_on_submit():
        pub = publications(publicationname=form.publicationname.data,description=form.description.data,guided=form.guided.data,url=form.url.data,pub=current_user)
        db.session.add(pub)
        db.session.commit()
        return redirect(url_for("postpublications"),code=301)
    return render_template("publication.html",title="Publications",form=form,pubadded=pubadded)

@app.route("/resume/new/skills",methods=['GET','POST'])
@login_required
def postskills():
    form = usersk()
    skillsadded = skills.query.filter_by(skill=current_user).all()
    if form.validate_on_submit():
        sk = skills(skillname=form.skillname.data,skill=current_user)
        db.session.add(sk)
        db.session.commit()
        return redirect(url_for("postskills"),code=301)
        #print(form.skillname.data)

    return render_template("skills.html",title="Skills",form=form,skillsadded=skillsadded)

@app.route("/resume/new/links",methods=['GET','POST'])
@login_required
def postlinks():
    form = userli()
    linksadded = links.query.filter_by(link=current_user).all()
    if form.validate_on_submit():
        sk = links(linkname=form.linkname.data,link=current_user)
        print(str( db.session.add(sk)))
        db.session.add(sk)
        db.session.commit()
        return redirect(url_for("postlinks"),code=301)
        #print(form.skillname.data)

    return render_template("links.html",title="Links",form=form,linksadded=linksadded)


@app.route("/resume/new/achieve",methods=['GET','POST'])
@login_required
def postachieve():
    form = achieve()
    achadded = achievements.query.filter_by(ach=current_user).all()
    if form.validate_on_submit():
        acheive = achievements(achname=form.achname.data,achdesc=form.achname.data,ach=current_user)
        db.session.add(acheive)
        db.session.commit()
        return redirect(url_for("home"),code=301)
        #print(form.skillname.data)

    return render_template("achieve.html",title="Achievements",form=form,achadded=achadded)
       


#delete

@app.route("/resume/new/education/<int:education_id>/delete",methods=["GET","POST"])
def delete_edu(education_id):
    eduview = education.query.get_or_404(education_id)

    db.session.delete(eduview)
    db.session.commit()
    flash('Your education detail post has been deleted!', 'success')
    return redirect(url_for('postedu'),code=301)



@app.route("/resume/new/experience/<int:experience_id>/delete",methods=["GET","POST"])
def delete_exp(experience_id):
    expview = experience.query.get_or_404(experience_id)

    db.session.delete(expview)
    db.session.commit()
    flash('Your experience detail post has been deleted!', 'success')
    return redirect(url_for('postexp'),code=301)

@app.route("/resume/new/projects/<int:project_id>/delete",methods=["GET","POST"])
def delete_pro(project_id):
    proview = projects.query.get_or_404(project_id)

    db.session.delete(proview)
    db.session.commit()
    flash('Your project detail post has been deleted!', 'success')
    return redirect(url_for('postprojects'),code=301)

@app.route("/resume/new/publications/<int:publication_id>/delete",methods=["GET","POST"])
def delete_pub(publication_id):
    proview = publications.query.get_or_404(publication_id)

    db.session.delete(proview)
    db.session.commit()
    flash('Your project detail post has been deleted!', 'success')
    return redirect(url_for('postpublications'),code=301)
    

@app.route("/resume/new/achieve/<int:achieve_id>/delete",methods=["GET","POST"])
def delete_achieve(achieve_id):
    achview = achievements.query.get_or_404(achieve_id)

    db.session.delete(achview)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('postachieve'),code=301)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,ext = os.path.splitext(form_picture.filename)
    pic = random_hex + ext
    path = os.path.join(app.root_path,'static/profiles',pic)
    
    output_size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(path)
    return pic

@app.route("/accounts",methods=['GET','POST'])
@login_required          #checks if user logged in or not and then allows access
def accounts():
    form= account()
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = save_picture(form.picture.data)
            current_user.picture = pic_file
        current_user.username = form.new_username.data
        current_user.email = form.new_email.data  # Update current user values
        db.session.commit()
        flash("Your Account has been updated","success")
        return redirect(url_for("accounts"),code=301)
    elif request.method == 'GET':
        form.new_username.data = current_user.username
        form.new_email.data = current_user.email
    image_file = url_for('static',filename='profiles/'+ current_user.image_file)
    return render_template("account.html",title="Account",image_file=image_file,form=form)


@app.route("/download",methods=["GET"])
@login_required
def downloadpdf():
    edu = education.query.filter_by(edu=current_user).all()
    exp = experience.query.filter_by(exp=current_user).all()
    pro = projects.query.filter_by(pro=current_user).all()
    pub = publications.query.filter_by(pub=current_user).all()
    usr = userdetails.query.filter_by(details=current_user).first()
    skillsadded = skills.query.filter_by(skill=current_user).all()
    linksadded = links.query.filter_by(link=current_user).all()
    achmade = achievements.query.filter_by(ach=current_user).all()

    image_file = url_for('static',filename='profiles/'+ current_user.image_file)
    css = ["resume/static/resume.css","resume/static/main.css"]
    rendered = render_template("resume.html",edu=edu,exp=exp,pro=pro,pub=pub,usr=usr,sk=skillsadded,li=skillsadded,achmade=achmade,image_file=image_file)
    options = {'enable-local-file-access': None}

    pdf =pdfkit.from_string(rendered,False,css=css,options=options)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachement; filename=resume.pdf"

    return response



@app.route("/resume",methods=["GET","POST"])
@login_required
def resumeview():
    edu = education.query.filter_by(edu=current_user).all()
    exp = experience.query.filter_by(exp=current_user).all()
    pro = projects.query.filter_by(pro=current_user).all()
    pub = publications.query.filter_by(pub=current_user).all()
    usr = userdetails.query.filter_by(details=current_user).first()
    skillsadded = skills.query.filter_by(skill=current_user).all()
    linksadded = links.query.filter_by(link=current_user).all()
    achmade = achievements.query.filter_by(ach=current_user).all()
    

    image_file = url_for('static',filename='profiles/'+ current_user.image_file)

    return render_template("resume.html",edu=edu,exp=exp,pro=pro,pub=pub,usr=usr,sk=skillsadded,li= linksadded,achmade=achmade,image_file=image_file)