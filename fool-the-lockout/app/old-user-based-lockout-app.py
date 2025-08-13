from flask import Flask, render_template, request, redirect, url_for, session, make_response
import time
import secrets
import json


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

user_db = {}    
""" format ->
    username:{
       "password" : string,
       "lockout_until" : int      # -1 if not locked out, timestamp of lockout end
    } 
"""
login_attempts = {}
""" format ->
    "username":{
        "tries": int
        "interval_start": timestamp
    }
"""
MAX_ATTEMPTS = 5      # max failed attempts before a user is locked out
ATTEMPT_EPOCH = 120     # timeframe for failed attempts (in seconds)
LOCKOUT_DURATION = 300      # duration a user will be locked out for (in seconds)
 


## ------------------------ HELPER FUNCTIONS ------------------------ ##

""" Quick function to no-cache web page responses"""
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response


"""Returns true if a user is logged in, false otherwise"""
def logged_in():
    if "user" in session:
        return True
    return False


"""Returns the current user (or None if there is none)"""
def current_user():
    if "user" in session:
        return session["user"]
    return None


"""Add a new user to db"""
def add_new_user(username, password):
    user_db[username] = {"password":password, "lockout_until":-1}
    print("Added (username=%s, password=%s) to user_db" % (username, password))


"""Checked if user is locked out, and if so if lock out period has expired.  If the
lockout period has expired, will update user_db to reflect change.  Returns true only
when user is actively locked out."""
def sync_n_check_if_lockedout(username):
    lockout_end = user_db[username]["lockout_until"]
    # if not locked out return False
    if lockout_end == -1:
        return False

    # if was locked out but period ended update store and return False
    if time.time() >= lockout_end:
        user_db[username]["lockout_until"] = -1
        return False

    # otherwise return True
    return True


"""Removed user from login_attempts db if possible"""
def clear_login_attemps(username):
    if username in login_attempts:
        del login_attempts[username]


"""Checks the current number of attempts for this username in the given epoch.
If the epoch has since passed, it clears the user entry from login_attempts db."""
def sync_user_attemps(username):
    curr_time = time.time()
    if username not in login_attempts:
        return

    # check if attempt interval has elapsed
    epoch_start_time = login_attempts[username]["epoch_start"] 
    if curr_time - epoch_start_time > ATTEMPT_EPOCH:
        clear_login_attemps(username)


"""Updates login_attempts db with new failed attempt,  If this is the first attempt
in the attempt interval it marks the time the interval began.  ALso locks out the user
if max attempts have been reached."""
def record_failed_login(username):
    # log bad password attempt
    if username not in login_attempts:
        login_attempts[username] = {"tries":1, "epoch_start":time.time()}
    else:
        login_attempts[username]["tries"] += 1

    # check whether to lockout user
    if MAX_ATTEMPTS - login_attempts[username]["tries"] <= 0:
        user_db[username]["lockout_until"] = time.time() + LOCKOUT_DURATION


# TODO - could do a daemon, but since checks of status are always done before
# updating its not really necessary


## ------------------------  APP ROUTES ------------------------ ##

""" Login portal """
@app.route("/login", methods=['GET', 'POST'])
def login():
    # if POST, accept form data and try to add user
    if request.method == "POST":
        user_input = request.form['username']
        pswd_input = request.form['password']
        print("User input: %s, password input: %s" % (user_input, pswd_input))

        # non-existent user
        if (user_input not in user_db):
            return render_template('login.html', error="User doesnt exist")

        # if locked out, dont even register attempt
        if sync_n_check_if_lockedout(user_input):
            msg = f"User is locked out for {LOCKOUT_DURATION/60} minutes!"
            return render_template("login.html", error=msg)

        # wrong password, log attempt
        sync_user_attemps(user_input)
        if (user_db[user_input]["password"] != pswd_input):
            record_failed_login(user_input)
            if not sync_n_check_if_lockedout(user_input):
                tries_left = MAX_ATTEMPTS - login_attempts[user_input]["tries"] 
                msg = f"Invalid username or password. Attempts left: {tries_left}"
                return render_template("login.html", error=msg)
            else:
                msg = f"Max attempts reached! Locked out for {LOCKOUT_DURATION/60} minutes!"
                return render_template("login.html", error=msg)
        
        # authenticate user
        session["user"] = user_input        # set current session in browser
        clear_login_attemps(user_input)
        print("Successfully logged in, session=%s" % (session))
        return redirect(url_for("index"))       # note 'index' refers to the FUNCTION NAME
        
    # return normal page if 'GET'
    return no_cache(make_response(render_template('login.html'))) 


""" Homepage """
@app.route("/", methods=['GET'])
def index():
    # client_ip = request.remote_addr
    # print(f"Request ip address: {client_ip}", flush=True)
    # authenticate
    if not logged_in():
        return redirect(url_for("login"))
    
     # display homepage according to login
    user = current_user()
    flag = "picoCTF{dummy_flag}"  #open("/challenge/flag.txt").read().strip
    return no_cache(make_response(render_template("index.html", user=user, flag=flag)))


""" Logout """
@app.route("/logout", methods=['GET'])
def logout():
    if "user" in session:
        session.pop('user', None)
        print("Logged out, popped session")
    return redirect(url_for("login"))


if __name__ == '__main__':
    username, password = None, None
    # get profile data
    try:
        with open("/challenge/profile.json", "r") as file:
            profile = json.load(file)
            username = profile["username"]
            password = profile["password"]
    except Exception as e:
        print(f"Error setting up profile in app:\n{e}")
        exit(1)

    # add new user
    add_new_user(username, password)
   
    # start app
    app.run(host='0.0.0.0', port=8000, debug=True)  