from flask import Flask, redirect, url_for, session, jsonify, render_template,request,make_response,jsonify,session
from flask_restful import Api, Resource
from authlib.integrations.flask_client import OAuth
import random
import os
import SQLite
import json
import configparser
import string
from sendMail import sendMail
from flask_session import Session


# Load configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Get environment variables using os.environ.get
CLIENT_ID = os.environ.get('CLIENT_ID') or config['DEFAULT']['CLIENT_ID']
CLIENT_SECRET = os.environ.get('CLIENT_SECRET') or config['DEFAULT']['CLIENT_SECRET']
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY') or config['DEFAULT']['APP_SECRET_KEY']
SECRET_KEY = os.environ.get('SECRET_KEY') or config['DEFAULT']['SECRET_KEY']
DEBUG = os.environ.get('DEBUG') or config['DEFAULT'].getboolean('DEBUG')

os.system("clear")
db = SQLite.SQLiteDatabase("users.db")
db.createTable();

def genOTP():
    digits = [random.randint(0, 9) for _ in range(6)]
    otp = int(''.join(map(str, digits)))
    return otp

# Store OTPs temporarily
otp_store = {"email":"","otp":""}  


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
api = Api(app)
oauth = OAuth(app)
Session(app)


google = oauth.register(
    name='google',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'},
)

@app.route('/')
def index():
    return render_template('login.html')

class Login(Resource):
    def get(self):
      return redirect("/")

    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        result  = db.verify_password(email,password)
        if result == True:
          session['user_id'] = email
          return True
        else:
          return False

class GoogleLogin(Resource):
    def get(self):
      return google.authorize_redirect(redirect_uri=api.url_for(AuthorizedResource, _external=True))          
        
class Register(Resource):
    def get(self):
      return make_response(render_template("register.html"))  

    def post(self):
        global otp_store
        name = request.form.get('name')
        email = request.form.get('email')
        otp = request.form.get('otp')
        password = request.form.get('password')
        data = {"name":name,"email":email,"password":password}
        if name and email and password:
          res = db.fetchByMail(email)
          if res == True:
            message = {"message":"Email alredy Exists"}
            return message
          else:
            if (int(otp) == int(otp_store["otp"]) and str(email)==str(otp_store["email"])):   
              uploadstats = db.insertData(name,email,password)
              return uploadstats
            else:
              message = {"message":"Inavlid OTP"}
              return (message) 

        else:
          message = {"message":"Data Fields Cant Be Empty"}
          return (message)  

class SendOtp(Resource):
    def get(self):
        global otp_store
        email = request.args.get('email')
        res = db.fetchByMail(email)
        if res == True:
          message = {"message":"Email Alredy Exists"}
          return (message)
        else:  
          otp_store["email"] = email
          otp_store["otp"] = genOTP()
          result = sendMail(email,otp_store["otp"])
          return result


class AuthorizedResource(Resource):
    def get(self):
        token = google.authorize_access_token()
        user_info = google.get('https://www.googleapis.com/oauth2/v2/userinfo')
        data = user_info.json()
        name = data["name"]
        email = data["email"]
        password = data["id"]
        res = db.fetchByMail(email)
        if res == True:
          result  = db.verify_password(email,password)
          if result == True:
            session['user_id'] = email
            return redirect("/home/")
          else:
            return redirect("/login/") 
        else:
          uploadstats = db.insertData(name,email,password)
          return redirect("/login/")

class Home(Resource):
    def get(self):
      user_id = session.get('user_id')
      if user_id:
        return make_response(render_template("home.html",user=user_id))
      else:
        return 'Not logged in'

class Logout(Resource):
    def get(self):
      #user_id = session.get('user_id')
      if 'user_id' in session:
        session.pop('user_id', None)  # Remove user_id from session
        return redirect("/")
      else:
        return redirect("/")

api.add_resource(Login, '/login/')
api.add_resource(GoogleLogin, '/googlelogin/')
api.add_resource(Logout, '/logout/')
api.add_resource(Home, '/home/')
api.add_resource(Register, '/register/')
api.add_resource(AuthorizedResource, '/authorized/')
api.add_resource(SendOtp, '/sendotp/')

if __name__ == '__main__':
    print(f"Running at: http://127.0.0.1:5000")
    app.run(debug=DEBUG,host='0.0.0.0')
