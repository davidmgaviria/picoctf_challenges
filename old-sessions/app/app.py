from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash, get_flashed_messages
from flask_session import Session
import sqlite3
import datetime
import secrets
import msgpack
from db_core import init_db, create_user, login_user, user_exists


app = Flask(__name__)

SESSIONS_DB_NAME = 'sessions.db'

# --- Initalize SQLAlchemy for server-side sessions ---
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{SESSIONS_DB_NAME}" 
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
app.config['SESSION_PERMANENT'] = True  
app.config['PERMANENT_SESSION_LIFETIME'] = 999999999    # effectively forever
app.config['SESSION_USE_SIGNER'] = False                # no session signing
Session(app)


## ------------- HELPER FUNCTIONS ------------- ##

""" Creates a session (gets stored in backend db)"""
def create_session(username):
    session['key'] = username


"""Get the current session id from the 'session' cookie in an HTTP request.
Only works when called right after an HTTP request with the cookie was recieved."""
def get_current_session() -> str:
    sid = request.cookies.get('session', None)
    print(f"Current session: {sid}")
    return sid


"""Checks if there is an existing session and if there is a user associated with it. If there 
is no  session, false is returned.  If the session is set but no user exists, instructs browser 
to clear the session and returns an error to the browser through 'str.'  Otherwise the username 
of the current user is returned. """
def authenticate_user() -> (bool, str):
    # check if session exists
    sid = get_current_session()
    if sid == None:
        return False, None

    # check if a user exists for the session
    user = session.get('key', None)
    if user == None:
        session.clear()
        error = "Unable to login -- either the session was invalidated or the user was deleted.\nPlease login or register again."
        return False, error
    return True, user

""" Quick function to no-cache web page responses"""
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response


## -------------------------------------------- ##


""" Login portal """
@app.route("/login", methods=['GET', 'POST'])
def login():
    # if POST, accept form data and try to add user
    if request.method == "POST":
        username_input = request.form['username']
        password_input = request.form['password']

        # handle invalid credentials
        if not login_user(username_input, password_input):
            return render_template('login.html', error="Invalid username or password")

        # establish new session
        create_session(username_input)  
        print("Successfully logged in")
        return redirect(url_for("index"))

    # return normal page if 'GET' (check for flashed error msgs)
    errors = get_flashed_messages(category_filter=["error"])
    if errors:
        return render_template('login.html', error=errors[0])
    else:
        return render_template('login.html')


""" Register portal """
@app.route("/register", methods=['GET', 'POST'])
def register():
    # if POST, accept form data and try to add user
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        conf_password = request.form['conf_password']

        # handle possible errors
        if user_exists(username):
            return render_template('register.html', error="Username already in use")
        if username.lower()=="none" or username.lower()=="null":
            return render_template('register.html', error=f"Username cannot be {username}")
        if password != conf_password:
            return render_template('register.html', error="Password and 'confirm password' must match")

        # try to make user
        if create_user(username, password):
            return redirect(url_for("login"))
        else:
            return render_template('register.html', error="Something went wrong")
    
    # return normal page if 'GET'
    return render_template('register.html')


""" Homepage """
@app.route("/", methods=['GET'])
def index():
    # authenticate 
    loggedIn, msg = authenticate_user()
    if not loggedIn:
        flash(msg, "error")     # "error" is the category
        return redirect(url_for("login"))
    
    # display homepage according to login
    user = msg
    if user == "admin":
        flag = open("/challenge/flag.txt").read().strip()
    else:
        flag = None
    # send page
    response = make_response(render_template("index.html", user=user, flag=flag))
    return no_cache(response)


""" Logout """
@app.route("/logout", methods=['GET'])
def logout():
    if get_current_session() != None:
        session.clear()
    return redirect(url_for("login"))


""" Debug page with past logins """
@app.route("/sessions", methods=['GET'])
def display_sessions():
    # authenticate 
    loggedIn, msg = authenticate_user()
    if not loggedIn:
        flash(msg, "error")     # "error" is the category
        return redirect(url_for("login"))
    
    # read session db 
    error_msg = "<h1>500 Interal Server<h1><p>Something went wrong, please report to challenge devs</p>"
    try:
        db_path = f'instance/{SESSIONS_DB_NAME}'
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            SELECT * FROM sessions
        ''')
        rows = c.fetchall()
    except Exception as e:
        print("Unable to read sessions from the db: %s" % e)
        return error_msg
    finally:
        conn.close()

    # try to output session data
    try:
        output = ""
        for row in rows:  
            index = row[0]
            sess_sid = row[1]
            data = msgpack.unpackb(row[2], raw=False)   # unpack data
            output += f"<p>{index}) {sess_sid}, {data}</p>"
        return output
    except Exception as e:
        # set output as error
        print("[ERROR]: %s" % e)
        return error_msg
   

""" Health page to check app is active """
@app.route("/health", methods=['GET'])
def health():
    return "OK", 200


if __name__ == '__main__':
    # initalize database
    init_db()
    # start app
    app.run(host='0.0.0.0', port=8000)  