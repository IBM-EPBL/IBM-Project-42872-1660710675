import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dyh88301;PWD=883zC0JwxWY2ar40","", "")
if conn :
    print('connected')
else:
    print("failed to connect")

Server = ibm_db.server_info(conn)

id_list=[]
# print("DBS Name:", Server.DBMS_NAME)
# print("DB Version:", Server.DBMS_VER)
# print("DB Name:", Server.DB_NAME)

# createQuery = "create table Authentication (Username varchar(50) NOT NULL, Password varchar(20) NOT NULL)"

# create_table = ibm_db.exec_immediate(conn, createQuery)

def checkEmailExist(email):
    stmt = ibm_db.exec_immediate(conn, "select username from AUTHENTICATION where username='"+email+"';")
    entries = False
    while ibm_db.fetch_row(stmt) != False:
        entries = True
    return entries, "An Same Email is already Existing"

def createUserWithPassword(username, password):
    stmt = "insert into Authentication (Username, Password) values ('"+username+"', '"+ password+"');"
    if ibm_db.exec_immediate(conn, stmt):
        print("values Updated")

def getUsernameAndPasswords():
    stmt = ibm_db.exec_immediate(conn, "select * from Authentication")
    entries = 0
    while ibm_db.fetch_row(stmt) != False:
        entries += 1
        print("Username: ", ibm_db.result(stmt, 0))
    else:
        if(entries == 0):
            return "Not found"
    

def createUserProfile(name, email, number):
    stmt = "insert into UserProfileDetails (name , email , PhoneNumber) values ('"+name+"','"+email+"','"+number+"');"
    if ibm_db.exec_immediate(conn, stmt):
        print("values Inserted")

def loginUser(username, password):
    stmt = ibm_db.exec_immediate(conn, "select password from AUTHENTICATION where username='"+username+"';")
    entries = 0
    while ibm_db.fetch_row(stmt) != False:
        entries += 1
        value = ibm_db.result(stmt, 0)
        print("Password: ", value)
        DBpassword = value
        if DBpassword != password:
            print("password Incorect")
            return False
        else:            
            return True
    else:
        if(entries == 0):
            return "Not found"

def adminLogin(username,password):
    stmt=ibm_db.exec_immediate(conn,"select password from ADMIN where username='"+username+"';")
    entries = 0
    while ibm_db.fetch_row(stmt) != False:
        entries += 1
        value = ibm_db.result(stmt, 0)
        print("Password: ", value)
        DBpassword = value
        if DBpassword != password:
            print("password Incorect")
            return False, "password Incorect"
        else:            
            return True, "Success"
    else:
        if(entries == 0):
            return "Not found"

def createAdmin(username,password):
    stmt = "insert into ADMIN (username,password) values ('"+username+"','"+password+"');"
    if ibm_db.exec_immediate(conn, stmt):
        return True
    else:
        return False

def isAdminExist(email):
    print("is Admin?")
    stmt = ibm_db.exec_immediate(conn, "select username from ADMIN where username='"+email+"';")
    entries = False
    while ibm_db.fetch_row(stmt) != False:
        entries = True
    return entries, "An Same Email is already Existing"

def createStaff(name,email):
    stmt = "insert into staff (name,email) values ('"+name+"','"+email+"');"
    if ibm_db.exec_immediate(conn, stmt):
        return True
    else:
        return False


def post_query(id,username,query_desc):
    stmt="insert into QUERIES (id,username,query_desc) values ('"+id+"','"+username+"','"+query_desc+"');"
    if ibm_db.exec_immediate(conn,stmt):
        return True
    else:
        return False

def fetch_query():
    sql = "SELECT * FROM QUERIES"
    stmt = ibm_db.exec_immediate(conn, sql)
    s=""
    while ibm_db.fetch_row(stmt) != False:
        s+="<h3>"+ibm_db.result(stmt,1)+"</h3>"
        s+="<h4>"+ibm_db.result(stmt,2)+"</h4>"
        s+=fetch_staff()
    return s

def fetch_staff():
    sql="SELECT name FROM STAFF"
    stmt=ibm_db.exec_immediate(conn,sql)
    s="""<script>
        function myFunction() {
        alert("Staff assigned");
    }</script>"""
    s+="<label for='staff'>Choose a staff:</label>"
    s+="<select id='staffs'>"
    while(ibm_db.fetch_row(stmt)!=False):
        s+="<option>"+ibm_db.result(stmt,0)+"</option>"
    s+="</select>"
    s+="<button onclick='myFunction()'>Assign</button>"
    return s
