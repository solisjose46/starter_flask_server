from constants import *
from db_creds import *
from flask import Flask, redirect, url_for, request, send_from_directory, make_response, session
import mysql.connector
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

# configure the secret key for sessions
app.config["SECRET_KEY"] = SECRET_KEY["key"] 
# session lives even after user closes browser for 5 days
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=5)

# configure sql driver
connection = mysql.connector.connect(host=DB_CREDS['host'], user=DB_CREDS['username'], passwd=DB_CREDS['password'], database=DB_CREDS['database'])

# sql driver for db operations
db_cursor = connection.cursor()

# validate user login
def is_valid_user(username, password):
    statement = f"select password from users where username='{username}';"
    db_cursor.execute(statement)
    result = db_cursor.fetchone()

    if not result:
        return False

    # hash result[0] here

    if result[0] != password:
        return False
    
    return True

# checks if user exists
def user_exists(username):
    statement = f"select 1 from users where username='{username}';"
    db_cursor.execute(statement)
    result = db_cursor.fetchone()

    print(f"result {result}")

    if result:
        return True
    
    return False

def register_user(username, password):
    statement = f"insert into users (username, password) values ('{username}', '{password}');"
    db_cursor.execute(statement)
    connection.commit()
    # result = db_cursor.fetchone()
    # print(f"result: {result}")



@app.route('/', methods=['GET'])
def index():
    # if user does not have session then redirect to login
    if "user" not in session:
        return redirect(url_for("get_login"))
    
    # else serve index
    return send_from_directory(HTML_PATH["html"], "index.html")

@app.route('/logout', methods=['GET'])
def get_logout():

    # remove user's session if exists
    if "user" in session:
        session.pop("user", None)

    # then redirect to login
    return redirect(url_for("get_login"))

@app.route('/login', methods=['GET', 'POST'])
def get_login():

    # user is logged in
    if "user" in session:
        return redirect(url_for("index"))

    # return login page if get
    if request.method == "GET":
        return send_from_directory(HTML_PATH["html"], "login.html")

    # else is Post
    username = ""
    password = ""
     
    # blank form handling
    try:
        username = request.form.get("username")
        password = request.form.get("password")
    except Exception as e:
        return make_response(send_from_directory(HTML_PATH["html"], "login.html"), 401)
    
    # bad login handling
    if not is_valid_user(username, password):
        return make_response(send_from_directory(HTML_PATH["html"], "login.html"), 401)
    
    # good login
    # get user a session and return index
    session.permanent = True
    session["user"] = username 
    return send_from_directory(HTML_PATH["html"], "index.html")


@app.route('/register', methods=['GET', 'POST'])
def get_register():

    # user is logged in
    if "user" in session:
        print("already log in")
        return redirect(url_for("index"))

    # if get return the register page
    if request.method == "GET":
        return send_from_directory(HTML_PATH["html"], "register.html")

    # else is Post
    username = ""
    password = ""
    confirm_password = ""
     
    # blank form handling
    try:
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
    except Exception as e:
        return make_response(send_from_directory(HTML_PATH["html"], "register.html"), 401)

    # passwords do not match
    if confirm_password != password:
        print("passwords do not match")
        return make_response(send_from_directory(HTML_PATH["html"], "register.html"), 401)

    # check if user already exists
    if user_exists(username):
        print("user exists!")
        return make_response(send_from_directory(HTML_PATH["html"], "register.html"), 401)
    
    print("user dne!")
    # user does not exist, make user and redirect to login
    # create user and redirect to login
    register_user(username, password)
    print("redirect to login")

    return redirect(url_for("get_login"))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)