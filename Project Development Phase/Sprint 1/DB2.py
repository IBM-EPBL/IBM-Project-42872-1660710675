from ibm_db import connect,server_info,exec_immediate,fetch_row,result

conn = connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dyh88301;PWD=883zC0JwxWY2ar40","", "")
if conn :
    print('connected')
else:
    print("failed to connect")

Server = server_info(conn)

# print("DBS Name:", Server.DBMS_NAME)
# print("DB Version:", Server.DBMS_VER)
# print("DB Name:", Server.DB_NAME)

# createQuery = "create table Authentication (Username varchar(50) NOT NULL, Password varchar(20) NOT NULL)"

# create_table = exec_immediate(conn, createQuery)

def checkEmailExist(email):
    stmt = exec_immediate(conn, "select username from AUTHENTICATION where username='"+email+"';")
    entries = False
    while fetch_row(stmt) != False:
        entries = True
    return entries, "An Same Email is already Existing"

def createUserWithPassword(username, password):
    stmt = "insert into Authentication (Username, Password) values ('"+username+"', '"+ password+"');"
    if exec_immediate(conn, stmt):
        print("values Updated")

def getUsernameAndPasswords():
    stmt = exec_immediate(conn, "select * from Authentication")
    entries = 0
    while fetch_row(stmt) != False:
        entries += 1
        print("Username: ", result(stmt, 0))
    else:
        if(entries == 0):
            return "Not found"
    

def createUserProfile(name, email, number):
    stmt = "insert into UserProfileDetails (name , email , number) values ('"+name+"','"+email+"','"+number+"');"
    if exec_immediate(conn, stmt):
        print("values Inserted")

def loginUser(username, password):
    stmt = exec_immediate(conn, "select password from AUTHENTICATION where username='"+username+"';")
    entries = 0
    while fetch_row(stmt) != False:
        entries += 1
        value = result(stmt, 0)
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
