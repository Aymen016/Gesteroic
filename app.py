from flask import Flask, render_template, session, redirect,flash, url_for,request
from functools import wraps
import pymongo
from user.routes import user_bp  # Import the Blueprint


app = Flask(__name__)

client = pymongo.MongoClient('localhost', 27017)
db = client['signhub']
students_db = client['students']  # New database for student info

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
  student = session.get('student', {})  # Avoids UndefinedError

  return render_template('dashboard.html', student=student)



@app.route("/register_student", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        student_data = {
            "_id": request.form["student_id"],
            "name": request.form["name"],
            "roll_number": request.form["roll_number"],
            "age": int(request.form["age"]),
            "profile_picture": request.form["profile_picture"],  # URL or file path
            "courses_enrolled": request.form.getlist("courses_enrolled"),
            "completed_courses": request.form.getlist("completed_courses"),
            "videos_watched": request.form.getlist("videos_watched"),
            "stats": {
                "total_courses": int(request.form["total_courses"]),
                "completed_courses": int(request.form["completed_courses"]),
                "progress": request.form["progress"]
            }
        }

        # Insert into MongoDB
        db.students.insert_one(student_data)
        flash("Student registered successfully!", "success")
        return redirect(url_for("register_student"))

    return render_template("register_student.html")

@app.route("/student_portal")
def student_portal():
    students = list(db.students.find())  # Fetch all students from MongoDB
    return render_template("student_portal.html", students=students)

if __name__ == "__main__":
  app.run(debug=True)