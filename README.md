# 🤟 GESTEROIC – Empowering the Deaf Community through Sign Language Learning

**GESTEROIC** is an online learning platform designed to help the **deaf community** in Pakistan (and globally) to **learn Pakistan Sign Language (PSL)** through video lectures, interactive quizzes, and progress tracking. It also features **SignHub**, a crowdsourcing portal for gesture uploads, enabling community contribution and collaboration.

## 🌐 Live Preview

🚀 [Visit GESTEROIC (Demo Link)](https://your-deployment-link.com)  
📽️ [Project Walkthrough Video](https://www.youtube.com/watch?v=your_demo_video_link)

---

## 📸 Screenshots

### 👨‍🏫 Admin Dashboard
![Admin Dashboard](screenshots/admin_dashboard.png)

### 📚 Course and Lectures View
![Courses Page](screenshots/courses_page.png)

### 👨‍🎓 Student Dashboard
![Student Dashboard](screenshots/student_dashboard.png)

### 🤲 SignHub Crowdsourcing Platform
![SignHub](screenshots/signhub.png)

---

## ✨ Features

### 🎓 Student Panel
- Register and login
- Browse available **courses** and **lectures**
- Watch video content
- Attempt quizzes and receive instant results
- **Track progress** with dashboard insights
- Receive **certificates** upon completion

### 👨‍💼 Admin Panel
- Admin registration and login
- Add/edit/delete:
  - Courses
  - Lectures (with video URLs)
  - Quizzes
- View platform stats: total users, total courses, lectures, quizzes
- Manage teacher assignments

### 🤲 SignHub - Gesture Crowdsourcing
- Upload sign language gesture videos
- View community submissions
- Encourage collaborative learning

---

## 🧑‍💻 Tech Stack

| Category       | Tools/Frameworks                                    |
|----------------|-----------------------------------------------------|
| Frontend       | HTML5, CSS3, Bootstrap, Jinja2                      |
| Backend        | Flask (Python)                                      |
| Database       | MongoDB (with PyMongo)                              |
| Hosting        | GitHub + Render / Railway (or your deployed server) |
| APIs/Packages  | OpenAI API (for medical chatbot module), YouTube    |

---

## 🗂️ Folder Structure

```bash
gesteroic/
│
├── static/
│   ├── css/
│   └── uploads/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── courses.html
│   ├── lectures.html
│   ├── quizzes.html
│   └── admin/
│
├── app.py
├── db_config.py
├── requirements.txt
└── README.md
