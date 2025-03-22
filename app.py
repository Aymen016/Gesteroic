from flask import Flask, render_template, session, redirect,flash, url_for,request
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pymongo
from user.routes import user_bp  # Import the Blueprint


app = Flask(__name__)

client = pymongo.MongoClient('localhost', 27017)
db = client['signhub']
students_db = client['students']  # New database for student info
students_collection = client['student_account']
video_lessons_collection = db["video_lessons"]

app.secret_key = "d7948298fbf92c770ebc7f14bf6e878f6fedf35a7368c09edda37d8a4e36a538"
from user import routes

app.register_blueprint(user_bp, url_prefix='/user')

UPLOAD_FOLDER = 'static/videos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  return wrap

@app.route('/')
def main_page():
  return render_template('main-page.html')

@app.route('/home')
def home():
   return render_template('home.html')
   

@app.route('/dashboard/')
@login_required
def dashboard():
  #student = session.get('student', {})  # Avoids UndefinedError
    total_students = students_collection.count_documents({})  # Get total count of students
    students = list(students_collection.find())  # Fetch all students' data
    total_courses = courses_collection.count_documents({})
    total_lessons = video_lessons_collection.count_documents({})
    
    return render_template('admin_dashboard.html', students=students, total_students=total_students, total_courses=total_courses, total_lessons=total_lessons)



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

@app.route("/students")
def student_portal():
    students = list(db.students.find())  # Fetch all students from MongoDB
    return render_template("student_portal.html", students=students)

students_collection = db["students"]

@app.route("/signup_student", methods=["GET", "POST"])
def signup_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        profile_picture = request.form["profile_picture"]  # Accept profile pic URL

        password = generate_password_hash(request.form["password"])
        age = request.form["age"]
        roll_number = request.form["roll_number"]

        if students_collection.find_one({"email": email}):
            flash("Email already exists!", "danger")
            return redirect(url_for("signup_student"))

        student_data = {
            "name": name,
            "email": email,
            "password": password,
            "age": age,
            "roll_number": roll_number,
            "profile_picture": profile_picture,
            "courses": [],
            "videos_watched": []
        }
        students_collection.insert_one(student_data)
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for("login_student"))

    return render_template("signup_student.html")

@app.route("/login_student", methods=["GET", "POST"])
def login_student():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        student = students_collection.find_one({"email": email})
        if student and check_password_hash(student["password"], password):
            session["student_email"] = email
            flash("Login successful!", "success")
            return redirect(url_for("student_dashboard"))
        else:
            flash("Invalid email or password!", "danger")

    return render_template("login_student.html")

@app.route("/student_dashboard")
def student_dashboard():
    if "student_email" not in session:
        return redirect(url_for("login_student"))

    student = students_collection.find_one({"email": session["student_email"]})
    return render_template("dashboard.html", student=student)
@app.route("/logout_student")
def logout_student():
    session.pop("student_email", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login_student"))

courses_collection = db["courses"]  # Collection for courses

@app.route("/courses")
def courses():
    courses = courses_collection.find()
    return render_template("courses.html", courses=courses)

@app.route("/add-course", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        course_id = request.form["course_id"]
        name = request.form["name"]
        professor = request.form["professor"]
        description = request.form["description"]
        credits = int(request.form["credits"])
        duration = request.form["duration"]

        students_enrolled = request.form["students_enrolled"]

        course_data = {
            "course_id": course_id,
            "name": name,
            "professor": professor,
            "students_enrolled": students_enrolled,
            "description": description,
            "credits": credits,
            "duration": duration
        }
        
        courses_collection.insert_one(course_data)
        return redirect(url_for("courses"))
    
    return render_template("add_course.html")

@app.route('/upload_video', methods=['POST'])
def upload_video():
    topic = request.form.get('topic')
    course_id = request.form.get('course_id')
    course_name = request.form.get('course_name')

    if 'video_file' not in request.files:
        flash("No file part", "danger")
        return redirect(url_for('add_video'))

    file = request.files['video_file']

    if file.filename == '':
        flash("No selected file", "danger")
        return redirect(url_for('add_video'))

    if file and file.filename.endswith('.mp4'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Save video details in MongoDB
        video_data = {
            "topic": topic,
            "course_id": course_id,
            "course_name": course_name,
            "video_path": file_path
        }
        video_lessons_collection.insert_one(video_data)

        flash("Video uploaded successfully!", "success")
        return redirect(url_for('video_lessons'))

    flash("Invalid file format. Only MP4 allowed.", "danger")
    return redirect(url_for('add_video'))

@app.route("/video_lessons")
def video_lessons():
    videos = list(video_lessons_collection.find())
    return render_template("video_lessons.html", videos=videos)

@app.route("/add_video", methods=["GET", "POST"])
def add_video():
    if request.method == "POST":
        topic = request.form["topic"]
        course_id = request.form["course_id"]
        course_name = request.form["course_name"]
        file = request.files["mp4_video"]

        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)  # Save to 'static/videos/'

        # Store relative path in MongoDB
        video_url = file_path.replace("\\", "/")  # Converts Windows `\` to `/`

        video_data = {
            "topic": topic,
            "course_id": course_id,
            "course_name": course_name,
            "video_url": video_url  # Fix the URL
        }
        video_lessons_collection.insert_one(video_data)

    
    return render_template("add_video.html")


if __name__ == "__main__":
  app.run(debug=True)