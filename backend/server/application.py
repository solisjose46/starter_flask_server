import imp
from constants import *
from db_creds import *
from flask import Flask, redirect, url_for, request, send_from_directory, make_response, session
import mysql.connector
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = SECRET_KEY["key"] 
# session lives even after user closes browser
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=5)

connection = mysql.connector.connect(host=DB_CREDS['host'], user=DB_CREDS['username'], passwd=DB_CREDS['password'], database=DB_CREDS['database'])

db_cursor = connection.cursor()

def is_valid_user(username, password):
    statement = f"select password from users where username='{username}'"
    db_cursor.execute(statement)
    result = db_cursor.fetchone()

    if not result:
        return False

    # hash result[0] here

    if result[0] != password:
        return False
    
    return True


@app.route('/', methods=['GET'])
def index():
    # if not session; redirect to get /login
    if "user" not in session:
        return redirect(url_for("get_login"))
    
    #else serve index
    return send_from_directory(HTML_PATH["html"], "index.html")

@app.route('/logout', methods=['GET'])
def get_logout():
    if "user" in session:
        session.pop("user", None)

    return redirect(url_for("get_login"))

@app.route('/login', methods=['GET', 'POST'])
def get_login():

    # user is logged in
    if "user" in session:
        return redirect(url_for("index"))

    # This is purely for development. Your wsgi server should serve static files.
    if request.method == "GET":
        return send_from_directory(HTML_PATH["html"], "login.html")

    # Post

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)