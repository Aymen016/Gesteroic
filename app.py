from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo
from user.routes import user_bp  # Import the Blueprint


app = Flask(__name__)

client = pymongo.MongoClient('localhost', 27017)
db = client['signhub']
app.secret_key = "d7948298fbf92c770ebc7f14bf6e878f6fedf35a7368c09edda37d8a4e36a538"
from user import routes

app.register_blueprint(user_bp, url_prefix='/user')

def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  return wrap

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')


if __name__ == "__main__":
  app.run(debug=True)