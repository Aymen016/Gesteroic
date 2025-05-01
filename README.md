# 🤟 GESTEROIC – Empowering the Deaf Community through Sign Language Learning

**GESTEROIC** is an online learning platform designed to help the **deaf community** in Pakistan (and globally) to **learn Pakistan Sign Language (PSL)** through video lectures, interactive quizzes, and progress tracking. It also features **SignHub**, a crowdsourcing portal for gesture uploads, enabling community contribution and collaboration.

## 🌐 Live Preview

🚀 [Visit GESTEROIC (Demo Link)](https://your-deployment-link.com)  
📽️ [Project Walkthrough Video](https://github.com/user-attachments/assets/5ce321f4-1326-4d82-80eb-98ff36ae12e4)



---

## 📸 Screenshots

### 👨‍🏫 Admin Dashboard
![Admin Dashboard]![image](https://github.com/user-attachments/assets/dfacc28c-29f2-41a7-a54a-e96042aa7322)


### 📚 Course and Lectures View
![Courses Page]![image](https://github.com/user-attachments/assets/0132ef95-d7bc-4838-9427-1f0a4acfa459)


### 👨‍🎓 Student Dashboard
![Student Dashboard](https://github.com/user-attachments/assets/3a97d135-b165-49ac-8364-85720faa9518)



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
```
---

## ⚙️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/gesteroic.git
cd gesteroic
```
### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```


