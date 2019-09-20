# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 17:23:14 2019

@author: vasanthi
"""
# flask introduction
from flask import Flask,redirect,url_for,render_template,request
from flask_mail import Mail,Message
from random import randint
from project_database import Register,Base,User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import flash
from flask_login import LoginManager,login_user,current_user,logout_user,login_required,UserMixin

engine=create_engine('sqlite:///iii.db')
engine=create_engine('sqlite:///iii.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine   #binding to database tables
DBsession=sessionmaker(bind=engine)  # sessionmaker bind the data store in engine
session=DBsession()

app=Flask(__name__)


login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='vasanthiganji414@gmail.com'
app.config['MAIL_PASSWORD']='gvasi123'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

app.secret_key="vas"

mail=Mail(app)
otp=randint(000000,999999)

@app.route("/sample")

def demo():
    return " welcome to iiit nuzvid"

@app.route("/demo")

def d():
    return"<h1>WElCOME</h1>"
    
@app.route("/info/details")
def t():
    return"hello details"
    
@app.route("/details/<name>/<int:age>/<float:salary>")
def info(name,age,salary):
    return "hello {}, age is {},  salary is {}".format(name,age,salary)

@app.route("/admin")
def admin():
    return "hello admin"

@app.route("/staff")
def staff():
    return "hello staff"

@app.route("/student")
def student():
    return "hello student"

@app.route("/info/<name>")    # function redirect to other page
def admin_info(name):
    if name=="admin":
        return redirect(url_for('admin'))
    elif name=="staff":
        return redirect(url_for('staff'))
    elif name=="student":
        return redirect(url_for('student'))
    else:
        return "NO URL"
    
@app.route("/data/<name>/<int:age>/<float:salary>")
def demo_html(name,age,salary):
    return render_template('sample.html',n=name,a=age,s=salary)

#display the values in table format in html
@app.route("/table")
def info_html():
    s_no=17
    name="vasanthi"
    branch='cse'
    dept='student'
    return render_template('table.html',s_no=s_no,n=name,b=branch,d=dept)

# to add large amount of data
data=[{'s_no':326,'name':'vasanthi','branch':'IT','dept':'student'},{'s_no':378,'name':'myna','branch':'IT','dept':'student'}]
@app.route("/dummy_data")
def dummy():
        return render_template("data.html",dummy_data=data)
    
@app.route("/table/<int:number>")
def table(number):
        return render_template("tables.html",n=number)
    
@app.route("/file_upload", methods=['GET','POST'])
def file_upload():
    return render_template("fileupload.html")

@app.route("/success", methods=['GET','POST'])
def success():
    if request.method=='POST':
            f=request.files['file']
            f.save(f.filename)
            return render_template("success.html",f_name=f.filename)


# mail sending and otp generation

@app.route("/email", methods=['POST','GET'])
def email_send():
    return render_template("email.html")
@app.route("/email_verify", methods=['POST','GET'])
def verify_email():
    email=request.form['email']
    msg=Message("one time password", sender="vasanthiganji414@gmail.com", recipients=[email])
    msg.body=str(otp)
    mail.send(msg)
    return render_template("v_email.html")

@app.route("/email_success", methods=['POST','GET'])
def success_email():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        return render_template("email_success.html")
    return "Invalid OTP"

# display database record  in web browser

@app.route("/show")
@login_required
def showData():
    register=session.query(Register).all()    # register is variable name
    
    return render_template('show.html',reg=register)

@app.route("/form",methods=['POST','GET'])
def form():
    if request.method=='POST':
        newData=Register(name=request.form['name'],
            sur_name=request.form['sur_name'],
            mobile=request.form['mobile'],
            email=request.form['email'],
            branch=request.form['branch'],
            role=request.form['role'])
        session.add(newData)
        session.commit()
        flash("New data added {}".format(editedData.name))
        return redirect(url_for('showData'))
    else:
        return render_template("form.html")
    
@app.route("/edit/<int:register_id>",methods=['POST','GET'])
def editData(register_id):
    editedData=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':
        editedData.name=request.form['name']
        editedData.sur_name=request.form['sur_name']
        editedData.mobile=request.form['mobile']
        editedData.email=request.form['email']
        editedData.branch=request.form['branch']
        editedData.role=request.form['role']
        
        session.add(editedData)
        session.commit()
        return redirect(url_for('showData'))
    else:
        return render_template("edit.html", register=editedData)
    
    
@app.route("/delete/<int:register_id>",methods=['POST','GET'])
def deleteData(register_id):
    deletedData=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':
        
        session.delete(deletedData)
        session.commit()
        flash("data deleted {}".format(deletedData.name))
        
        return redirect(url_for('showData'))
    else:
        return render_template("delete.html", register=deletedData)

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/account",methods=['POST','GOT'])
@login_required
def account():
    return render_template("account.html")

@app.route("/register",methods=['POST','GOT'])
def register():
    if request.method=='POST':
        userData=User(name=request.form['name'],
        email=request.form['email'],
        password=request.form['password'])
        session.delete(deletedData)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template("register.html")



@app.route("/login",methods=['POST','GOT'])
@login_required
def login():
    if current_user.is_authenticated:
        return redirect(url_for('showData'))
    try:
        if request.method=='POST':
            user=session.query(User).filter_by(email=request.form['email'],password=request.form['password']).first()
            
            if user:
                login_user(User)
                return redirect(url_for('showData'))
            else:
                flash("Invalid login..")
        else:
            return render_template('login.html',title="login")
            
    except Exception as e:
         flash("Login Failed")
         
    else:
         return render_template('login.html',title='login')

 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))       
            
            
            
@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))          
            
            
@app.route("/navigator")
def nav():
       return render_template('navigation.html')




if __name__=='__main__':    #__main__ check with realtime project or not
    app.run(debug=True)