import random
from flask import Flask, render_template, request, jsonify, make_response, url_for,redirect
import os
import DB2

myapp=Flask(__name__)

@myapp.route('/')
def home():
    return render_template('index.html')

@myapp.route("/user_login")
def user_login():
    return render_template('login.html')
myapp.add_url_rule("/user_login","user_login",user_login)

@myapp.route("/user_signup")
def user_signup():
    return render_template('signup.html')
myapp.add_url_rule("/user_signup","user_signup",user_signup)

@myapp.route("/admin_login")
def admin_login():
    return render_template('admin_login.html')
myapp.add_url_rule("/admin_login","admin_login",admin_login)


@myapp.route("/admin_reg")
def admin_reg():
    return render_template('admin_reg.html')
myapp.add_url_rule("/admin_reg","admin_reg",admin_reg)

@myapp.route("/add_staff")
def add_staff():
    return render_template('add_staff.html')
myapp.add_url_rule("/add_staff","add_staff",add_staff)

@myapp.route("/query")
def query():
    return render_template('chatting.html')
myapp.add_url_rule('/query','query',query)

@myapp.route("/queries_corner")
def queries_corner():
    return DB2.fetch_query()
myapp.add_url_rule("/queries_corner","queries_corner",queries_corner)

@myapp.route("/admin_login",methods=['POST'])
def admin_login_data():
    Email = request.form['email']
    Password = request.form['password']
    logged, message = DB2.adminLogin(Email, Password)
    if logged:
        return render_template('admin_panel.html', email = Email, password = Password)
    else:
        resp = make_response(render_template('admin_login.html'))
        resp.set_cookie('Message', message)
        return resp

@myapp.route("/admin_reg")
def admin_reg_data():
    email = request.form['email']
    password = request.form['password']
    CPassword = request.form['confirmPassword']
    if email == ""  or password == "" or CPassword == "":
        return render_template('admin_reg.html' , error="Validation error")
    else:
        error, message = DB2.isAdminExist(email)
        if error == False:
            created=DB2.createAdmin(email, password)
            if created:
                return render_template('admin_login.html')
        else:
            resp = make_response(render_template('admin_reg.html'))
            resp.set_cookie('Message', message)
            return resp

@myapp.route('/user_login', methods=['POST'])
def user_login_data():
    Email = request.form['email']
    Password = request.form['password']
    logged= DB2.loginUser(Email, Password)
    if logged:
        return redirect(url_for('query'))
    else:
        resp = make_response(render_template('login.html'))
        return resp

@myapp.route('/signup', methods=['POST'])
def signup_data():
    name = request.form['name']
    email = request.form['email']
    number = request.form['number']
    password = request.form['password']
    CPassword = request.form['confirmPassword']
    if name == "" or email == "" or number == "" or password == "" or CPassword == "":
        return render_template('signup.html' , error="Validation error")
    else:
        error, message = DB2.checkEmailExist(email)
        if error == False:
            DB2.createAdmin(email, password)
            DB2.createUserProfile(name, email, number)
            DB2.getUsernameAndPasswords()
            return render_template('login.html')
        else:
            resp = make_response(render_template('signup.html'))
            resp.set_cookie('Message', message)
            return resp

@myapp.route('/add_staff', methods=['POST'])
def add_staff_data():
    name=request.form['name']
    email=request.form['email']
    added=DB2.createStaff(name,email)
    if added:
        return render_template('admin_panel.html')
    else:
        return render_template('add_staff.html')

@myapp.route('/query',methods=['POST'])
def query_data():
    username=request.form['username']
    query_desc=request.form['message']
    t=str(random.randint(1,100000))
    if t not in DB2.id_list:
        id=t
        DB2.id_list.append(id)
    isPosted=DB2.post_query(id,username,query_desc)
    if isPosted:
        return render_template('thankyou.html',id=id)
    else:
        return redirect(url_for("home"))



myapp.run(debug=True)