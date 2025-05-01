from flask import Flask, render_template, request, redirect, session, url_for, flash
from pymongo import MongoClient
from bson import ObjectId
import gridfs
import datetime
import bcrypt

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Use env variable in real apps

# MongoDB config
MONGO_URI = "mongodb+srv://amyhehehehe11:cb6qMqjcGcQy3jcp@gesteroic.erzda6z.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['gesteroic']

users = db['users']  # your users collection
courses = db['courses']
lectures = db['lectures']
progress = db['progress']
enrollments = db['enrollments']
assessments = db['assessments']
teachers = db['teacher']
students = db['students']
admins = db['admins']
fs = gridfs.GridFS(db)

# -------- Routes ----------

@app.route('/')
def index():
    return render_template('index.html')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if the file was uploaded
        if 'profile_pic' not in request.files:
            return "No profile picture uploaded", 400

        profile_pic = request.files['profile_pic']

        if profile_pic.filename == '':
            return "No file selected", 400

        if profile_pic and allowed_file(profile_pic.filename):
            filename = secure_filename(profile_pic.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            profile_pic.save(filepath)  # Save to /static/uploads

            # Check if user already exists
            if students.find_one({'username': username}):
                return render_template('login.html', message="User already exists!")

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            students.insert_one({
                'username': username,
                'email': email,
                'password': hashed_password,
                'profile_pic': filename  # Just store the filename
            })

            return redirect(url_for('login'))
        else:
            return "Invalid file type", 400

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['password']
        
        student = students.find_one({"username": email})
        
        if student :
            session['user_id'] = str(student['_id'])
            return redirect('/dashboard')
        else:
            return "Invalid username or password", 401
    return render_template('login.html')

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form['title']
        description = request.form['description']

        # Insert course into the 'courses' collection
        course = {
            'course_name': course_name,
            'description': description,
        }
        courses.insert_one(course)

        return redirect(url_for('index'))

    return render_template('add_course.html')

@app.route('/add_lecture/<course_id>', methods=['GET', 'POST'])
def add_lecture(course_id):
    if request.method == 'POST':
        lecture_title = request.form['lecture_title']
        lecture_video_url = request.form['lecture_video_url']
        description = request.form['description']

        # Insert lecture into the 'lectures' collection
        lecture = {
            'course_id': ObjectId(course_id),
            'lecture_title': lecture_title,
            'lecture_video_url': lecture_video_url,
            'description': description,
        }
        lectures.insert_one(lecture)

        return redirect(url_for('view_course', course_id=course_id))

    return render_template('add_lecture.html', course_id=course_id)

@app.route('/view_course/<course_id>')
def view_course(course_id):
    # Fetch the course
    course = courses.find_one({"_id": ObjectId(course_id)})
    
    # Fetch the lectures
    lectures_list = list(lectures.find({"course_id": ObjectId(course_id)}))
    
    # Debugging step: Print out course_id and lectures_list
    print(f"Course ID: {course_id}")
    print(f"Lectures List: {lectures_list}")
    
    return render_template('view_course.html', course=course, lectures=lectures_list,get_youtube_video_id=get_youtube_video_id)



from bson.objectid import ObjectId

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    student = students.find_one({"_id": ObjectId(user_id)})
    pic = students['profile_pic']
    if not student:
        return "Student not found", 404

    all_courses = courses.find()
    return render_template('dashboard.html', student=student, courses=all_courses, pic=pic)





@app.route('/course/<course_id>')
def course(course_id):
    course = courses.find_one({"_id": ObjectId(course_id)})
    return render_template('course.html', course=course)

@app.route('/lecture/<course_id>/<lecture_id>')
def lecture(course_id, lecture_id):
    lecture = lectures.find_one({"_id": ObjectId(lecture_id)})
    if 'user_id' in session and lecture:
        progress.update_one(
            {'user_id': session['user_id'], 'course_id': course_id},
            {'$addToSet': {'watched': lecture_id}},
            upsert=True
        )

    return render_template('lecture.html', lecture=lecture)
@app.route('/enroll/<course_id>', methods=['POST'])
def enroll_course(course_id):
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    # Check if already enrolled
    existing = db.enrollments.find_one({
        'user_id': ObjectId(user_id),
        'course_id': ObjectId(course_id)
    })

    if not existing:
        db.enrollments.insert_one({
            'user_id': ObjectId(user_id),
            'course_id': ObjectId(course_id)
        })

    return redirect(url_for('dashboard'))

@app.route('/student/home')
def student_home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    student_id = ObjectId(session['user_id'])  # 🔧 Fix applied here

    enrollments_list = list(enrollments.find({'user_id': student_id}))
    print("Session student_id:", session['user_id'])
    print("Enrollments:", enrollments_list)
    course_ids = [enr['course_id'] for enr in enrollments_list]
    print(course_ids)

    enrolled_courses_data = []

    for course_id in course_ids:
        course = courses.find_one({'_id': ObjectId(course_id)})
        all_lectures = list(lectures.find({'course_id': ObjectId(course_id)}))

        progress_doc = progress.find_one({
            'student_id': ObjectId(student_id),
            'course_id': ObjectId(course_id)
        })

        watched = set(progress_doc.get('watched_lectures', [])) if progress_doc else set()

        # Mark lectures
        for lec in all_lectures:
            lec['watched'] = str(lec['_id']) in watched

        total = len(all_lectures)
        watched_count = len(watched)
        percent_complete = round((watched_count / total) * 100, 2) if total > 0 else 0

        enrolled_courses_data.append({
            'course_id': str(course['_id']),
            'course_name': course['course_name'],
            'description': course.get('description', ''),
            'progress': percent_complete,
            'lectures': all_lectures
        })

    return render_template('student_home.html', enrolled_courses=enrolled_courses_data)

import re
import re

def get_youtube_video_id(url):
    # Regular expression to match YouTube video IDs
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(?:[^/]+/)*(?:v|e(?:mbed)?)\/([^"&?\/\s]*)'
    match = re.match(youtube_regex, url)
    if match:
        return match.group(4)
    return None
from urllib.parse import urlparse, parse_qs

# Function to extract YouTube video ID from URL
def get_youtube_video_idd(url):
    parsed_url = urlparse(url)
    if 'youtube.com' in parsed_url.netloc:
        query = parse_qs(parsed_url.query)
        video_id = query.get('v', [None])[0]
        return video_id
    return None

@app.route('/watch/<lecture_id>')
def watch_lecture(lecture_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    student_id = ObjectId(session['user_id'])
    lecture = lectures.find_one({'_id': ObjectId(lecture_id)})

    if not lecture:
        return "Lecture not found", 404

    course_id = lecture['course_id']

    # Track progress for watched lectures
    progress_doc = progress.find_one({
        'student_id': student_id,
        'course_id': course_id
    })

    if not progress_doc:
        progress.insert_one({
            'student_id': student_id,
            'course_id': course_id,
            'watched_lectures': [str(lecture['_id'])]  # Track this lecture as watched
        })
    else:
        watched_lectures = set(progress_doc.get('watched_lectures', []))
        watched_lectures.add(str(lecture['_id']))  # Mark this lecture as watched
        progress.update_one(
            {'_id': progress_doc['_id']},
            {'$set': {'watched_lectures': list(watched_lectures)}}
        )

    


    # Render the video within the platform
    return render_template('watch_lecture.html', lecture=lecture,get_youtube_video_id=get_youtube_video_id)



@app.route('/make_assessment', methods=['GET'])
def make_assessment():
    return render_template('make_assessment.html')

@app.route('/teacher_signup', methods=['GET', 'POST'])
def teacher_signup():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        course_id = request.form['course_id']  # selected from dropdown

        if teachers.find_one({'email': email}):
            return "Teacher already exists!"

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        teachers.insert_one({
            'name': name,
            'email': email,
            'password': hashed_pw,
            'course_id': ObjectId(course_id)
        })

        return redirect('/teacher_login')
    all_courses = list(db.courses.find())
    return render_template('teacher_signup.html', courses=all_courses)

@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        teacher = teachers.find_one({'email': email})

        if teacher and bcrypt.checkpw(password.encode('utf-8'), teacher['password']):
            session['teacher_id'] = str(teacher['_id'])
            return redirect(url_for('teacher_dashboard'))
        else:
            return "Invalid login", 401

    return render_template('teacher_login.html')

@app.route('/create_assessment/<course_id>', methods=['GET', 'POST'])
def create_assessment(course_id):
    if 'teacher_id' not in session:
        return redirect('/teacher_login')

    if request.method == 'POST':
        question = request.form['question']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        correct_option_index = int(request.form['correct_option'])

        # Map the index to the actual option value
        options = [option_a, option_b, option_c, option_d]
        correct_option = options[correct_option_index]

        # Insert assessment data for the course
        assessments.insert_one({
            'course_id': ObjectId(course_id),
            'question': question,
            'options': options,
            'correct_option': correct_option,  # Store actual option value
            'teacher_id': ObjectId(session['teacher_id'])
        })

        return redirect(url_for('teacher_dashboard'))

    return render_template('create_assessment.html', course_id=course_id)


@app.route('/take_assessment/<course_id>', methods=['GET', 'POST'])
def take_assessment(course_id):
    # Convert course_id back to ObjectId
    course_id = ObjectId(course_id)
    
    # Fetch the course for the specific course_id
    course = courses.find_one({'_id': course_id})
    if not course:
        return "Course not found", 404

    # Fetch all the questions for the course_id (including correct_option)
    questions = list(assessments.find({'course_id': course_id}, {'question': 1, 'options': 1, 'correct_option': 1}))
    question_count = len(questions)

    if not questions:
        return "No assessment available for this course", 404

    if request.method == 'POST':
        student_answers = request.form.to_dict()
        result = calculate_score(student_answers, questions)

        # Pass score via query string to /enter_name
        return redirect(url_for('enter_name', course_id=course_id, score=result))



    return render_template('take_assessment.html', course=course, questions=questions, question_count=question_count)


def calculate_score(student_answers, questions):
    correct_answers = 0
    total_questions = len(questions)

    for index, question in enumerate(questions):
        correct_answer = question['correct_option']
        question_id = str(question['_id'])  # match the name used in the form (e.g., q<question_id>)
        student_answer = student_answers.get(f'q{question_id}')

        # Debug Print
        print(f"Question: {question['question']}")
        print(f"Student selected: {student_answer}")
        print(f"Correct answer: {correct_answer}")
        print("-" * 40)

        if student_answer == correct_answer:
            correct_answers += 1

    return (correct_answers / total_questions) * 100


from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/enter_name/<course_id>', methods=['GET', 'POST'])
def enter_name(course_id):
    score = request.args.get('score')

    if request.method == 'POST':
        student_name = request.form['student_name']
        profile_pic = request.files['profile_pic']

        # Save the image to static/uploads
        if profile_pic:
            filename = secure_filename(profile_pic.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profile_pic.save(filepath)
            profile_url = url_for('static', filename='uploads/' + filename)
        else:
            profile_url = None

        return redirect(url_for('report_card', course_id=course_id, score=score, student_name=student_name, profile_pic=profile_url))

    return render_template('enter_name.html', score=score, course_id=course_id)


@app.route('/report_card/<course_id>')
def report_card(course_id):
    course = courses.find_one({'_id': ObjectId(course_id)})
    if not course:
        return "Course not found", 404

    score = request.args.get('score')
    student_name = request.args.get('student_name')
    profile_pic = request.args.get('profile_pic')

    return render_template('report_card.html', course=course, score=score, student_name=student_name, profile_pic=profile_pic)


from flask import Flask, request, render_template, send_file
from PIL import Image, ImageDraw, ImageFont

TEMPLATE_PATH = "PIC.png"  # Path to your certificate template
OUTPUT_FOLDER = "certificates/"  # Folder to save generated certificates
FONT_PATH = "arialbd.ttf"  # Path to your font file
FONT_SIZE = 60
TEXT_COLOR = (0, 0, 0)  # Black color for the text

@app.route('/view_certificate')
def view_certificate():
    student_name = request.args.get('student_name')  # Get student_name from query parameter

    if not student_name:
        return "Student name is required", 400

    # Open the certificate template
    img = Image.open(TEMPLATE_PATH)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Calculate text position
    text_bbox = draw.textbbox((0, 0), student_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    image_width, image_height = img.size
    x = (image_width - text_width) / 2  # Center the text horizontally
    y = (image_height - text_height) / 2 - 100  # Adjust Y position based on your design

    # Add only the name to the certificate
    draw.text((x, y), student_name, fill=TEXT_COLOR, font=font)

    # Save the certificate
    output_path = os.path.join(OUTPUT_FOLDER, f"{student_name}_certificate.png")
    img.save(output_path)

    # Return the generated certificate as an attachment
    return send_file(output_path, as_attachment=True)

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'teacher_id' not in session:
        return redirect('/teacher_login')

    # Fetch teacher's data
    teacher = teachers.find_one({"_id": ObjectId(session['teacher_id'])})
    if not teacher:
        return "Teacher not found", 404

    # Fetch the course associated with the teacher
    course = courses.find_one({"_id": teacher.get('course_id')})
    if not course:
        return "Course not found for this teacher", 404

    # Count the number of lectures
    num_lectures = lectures.count_documents({"course_id": course['_id']})

    # Count number of enrolled students using enrollments table
    num_students = enrollments.count_documents({"course_id": course['_id']})

    return render_template('teacher_dashboard.html', 
                           teacher=teacher,
                           course=course, 
                           num_lectures=num_lectures, 
                           num_students=num_students)


@app.route('/view_students/<course_id>')
def view_students(course_id):
    course_id_obj = ObjectId(course_id)

    # Step 1: Get course and its lectures
    course = courses.find_one({"_id": course_id_obj})
    all_lectures = list(lectures.find({"course_id": course_id_obj}))
    total_lectures = len(all_lectures)

    # Step 2: Get all enrolled student IDs
    enrollments_cursor = enrollments.find({"course_id": course_id_obj})
    student_ids = [enr['user_id'] for enr in enrollments_cursor]

    # Step 3: Get student details
    students_cursor = students.find({"_id": {"$in": student_ids}})
    students_list = []

    for student in students_cursor:
        student_id = student['_id']

        # Step 4: Find progress doc for this student and course
        progress_doc = progress.find_one({
            "student_id": student_id,
            "course_id": course_id_obj
        })

        watched = set(progress_doc.get('watched_lectures', [])) if progress_doc else set()
        watched_count = len(watched)

        percent_complete = round((watched_count / total_lectures) * 100, 2) if total_lectures > 0 else 0
        student['progress'] = percent_complete

        students_list.append(student)

    return render_template("view_students.html", students=students_list, course=course)





@app.route('/quiz/<course_id>', methods=['GET', 'POST'])
def quiz(course_id):
    course = courses.find_one({"_id": ObjectId(course_id)})
    quiz = course.get("quiz", {})

    if request.method == 'POST':
        score = 0
        for q in quiz['questions']:
            selected = request.form.get(q['id'])
            if selected == q['answer']:
                score += 1

        progress.update_one(
            {'user_id': session['user_id'], 'course_id': course_id},
            {'$set': {'quiz_score': score}},
            upsert=True
        )

        return f"You scored {score}/{len(quiz['questions'])}"

    return render_template('quiz.html', quiz=quiz)

from werkzeug.security import generate_password_hash, check_password_hash
@app.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect('/admin_signup')

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)
        db.admins.insert_one({'email': email, 'password': hashed_password})
        flash('Signup successful! You can now log in.')
        return redirect('/admin_login')

    return render_template('admin_signup.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Debugging: print the email and password to see if they are correct
        print(f"Email: {email}, Password: {password}")

        admin = db.admins.find_one({'email': email})
        
        if admin:
            # Debugging: print the stored password hash
            print(f"Stored password hash: {admin['password']}")
            
            if check_password_hash(admin['password'], password):
                session['admin_id'] = str(admin['_id'])
                print('in')
                return redirect(url_for('admin_dashboard'))  # fixed the URL
            else:
                flash('Invalid credentials, please try again.')
        else:
            flash('No admin found with that email.')

        return redirect('/admin_login')

    return render_template('admin_login.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    # You can also print the session to ensure the admin is logged in
    print(f"Logged in admin ID: {session['admin_id']}")

    total_students = db.students.count_documents({})
    total_courses = db.courses.count_documents({})
    total_teachers = db.teacher.count_documents({})
    total_lectures = db.lectures.count_documents({})

    return render_template('admin_dashboard.html',
                           total_students=total_students,
                           total_courses=total_courses,
                           total_teachers=total_teachers,
                           total_lectures=total_lectures)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin_login'))
@app.route('/students')
def students_list():
    students = db.students.find()
    students_data = []

    for student in students:
        print(student)
        enrollmentss = db.enrollments.find({'user_id': student['_id']})
        print(enrollmentss)
        course_names = []
        for enrollment in enrollmentss:
            course = db.courses.find_one({'_id': enrollment['course_id']})  # Returns a single document
            print(course)
            if course:
                course_names.append(course['course_name'])  # Use actual field name

        students_data.append({
            'name': student['username'],  # assuming 'username' is the field
            'courses': ', '.join(course_names)
        })

    return render_template('students.html', students=students_data)

@app.route('/courses')
def view_courses():
    courses_list = []
    for course in db.courses.find():
        # Find teacher(s) who teach this course (since teachers have course_id)
        teacher = db.teacher.find_one({'course_id': course['_id']})
       # print(teacher)
        lectures = list(db.lectures.find({'course_id': course['_id']}))
        print(lectures)
        courses_list.append({
            'course_name': course['course_name'],
            'teacher_name': teacher['name'] if teacher else 'Unknown',
            'lectures': lectures
        })
    return render_template('courses.html', courses=courses_list)


@app.route('/lectures')
def view_lectures():
    lecture_list = []
    for lec in db.lectures.find():
        course = db.courses.find_one({'_id': lec['course_id']})
        lecture_list.append({
            'title': lec['lecture_title'],
            'course_name': course['course_name'] if course else 'Unknown'
        })
    return render_template('lectures.html', lectures=lecture_list)

@app.route('/teachers')
def view_teachers():
    teacher_list = []
    
    for teacher in db.teacher.find():
        # Check if teacher has a 'course_id' field
        course = db.courses.find_one({'_id': teacher.get('course_id')})
        print(course)
        teacher_list.append({
            'name': teacher['name'],
            'course_name': course['course_name'] if course else 'None'
        })
    
    return render_template('teachers.html', teachers=teacher_list)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

