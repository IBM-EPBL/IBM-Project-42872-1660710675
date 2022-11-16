from curses import window
from flask_socketio import SocketIO, send, emit
from flask import Flask, render_template, request, jsonify, make_response
import flask
import os
import DB2

app = Flask(__name__)

app.config['SECRET'] = "secret!123"
socketio = SocketIO(app, cors_allowed_origins="*")

dict_user = {'12345':{},'54321':{}}

@socketio.on('message')
def handle_message(message):
    if message != "User connected!":
        message = message.split(" ",1)
        send(message, broadcast=True)

#handle user to server
def add_user(req,email,session):
    if req not in dict_user:
        return False
    if len(dict_user[req]) == 2:
        print("cannot add session")
        return False
    else:
        dict_user[req][email] = session
        return True

@socketio.on('username', namespace='/private')
def recieve_username(Data):
    result = add_user(Data['session_id'],Data['email'],request.sid)
    print(request.sid)
    if result == True:
        print("User added!")
    if Data['session_id'] in dict_user:
        for server_client in dict_user[Data['session_id']]:
            if(server_client != Data['email']):
                print("sent = "+server_client)
                emit('server_client',server_client)

@socketio.on('private_message', namespace='/private')
def private_message(Values):
    recieve_session = dict_user[Values['session_id']][Values['email']]
    message = Values['message']
    emit('recieve_private_message', message, room=recieve_session)
@app.route("/chat")
def Chat():
    return render_template("chatting.html")

app.add_url_rule("/Chat","Chat",Chat)

picFolder = os.path.join('static','Images')
    
app.config['UPLOAD_FOLDER'] = picFolder

@app.route("/signup")
def signup():
    return render_template('signup.html')
    
app.add_url_rule("/signup","signup",signup)

@app.route("/login")
def login():
    return render_template('login.html')

app.add_url_rule("/login","login",login)
@app.route("/customer")
def customer():
    return render_template('customer.html') 

app.add_url_rule("/customer","customer",customer)

@app.route("/")
def home():
    return render_template('index.html', favicon = os.path.join(app.config["UPLOAD_FOLDER"], 'fav.png'))

@app.route("/admin_login")
def admin_login():
    return render_template('admin_login.html')
app.add_url_rule("/admin_login","admin_login",admin_login)


@app.route("/admin_reg")
def admin_reg():
    return render_template('admin_reg.html')
app.add_url_rule("/admin_reg","admin_reg",admin_reg)

@app.route("/add_staff")
def add_staff():
    return render_template('add_staff.html')
app.add_url_rule("/add_staff","add_staff",add_staff)

@app.route("/admin_login",methods=['POST'])
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

@app.route("/admin_reg")
def admin_reg_data():
    email = request.form['email']
    password = request.form['password']
    CPassword = request.form['confirmPassword']
    if email == ""  or password == "" or CPassword == "":
        return render_template('admin_reg.html' , error="Validation error")
    else:
        error, message = DB2.isAdminExist(email)
        if error == False:
            created,msg=DB2.createAdmin(email, password)
            if created:
                return render_template('admin_login.html')
        else:
            resp = make_response(render_template('admin_reg.html'))
            resp.set_cookie('Message', message)
            return resp

@app.route('/login', methods=['POST'])
def login_data():
    Email = request.form['email']
    Password = request.form['password']
    logged, message = DB2.loginUser(Email, Password)
    if logged:
        return render_template('chatting.html', email = Email, password = Password)
    else:
        resp = make_response(render_template('login.html'))
        resp.set_cookie('Message', message)
        return resp

@app.route('/signup', methods=['POST'])
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

@app.route('/add_staff', methods=['POST'])
def add_staff_data():
    name=request.form['name']
    email=request.form['email']
    added=DB2.createStaff(name,email)
    if added:
        return render_template('admin_panel.html')
    else:
        return render_template('add_staff.html')
if __name__  == '__main__':
    socketio.run(app, host="localhost")
