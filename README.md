# 🤟 GESTEROIC – Empowering the Deaf Community through Sign Language Learning

**GESTEROIC** is an online learning platform designed to help the **deaf community** in Pakistan (and globally) to **learn Pakistan Sign Language (PSL)** through video lectures, interactive quizzes, and progress tracking. It also features **SignHub**, a crowdsourcing portal for gesture uploads, enabling community contribution and collaboration.

## 🌐 Live Preview

📽️ [Project Walkthrough Video](https://github.com/user-attachments/assets/5ce321f4-1326-4d82-80eb-98ff36ae12e4)

---

## 📸 Screenshots

### 👨‍🏫 Admin Dashboard
![Admin Dashboard](https://github.com/user-attachments/assets/dfacc28c-29f2-41a7-a54a-e96042aa7322)


### 📚 Course and Lectures View
![Courses Page](https://github.com/user-attachments/assets/0132ef95-d7bc-4838-9427-1f0a4acfa459)


### 👨‍🎓 Student Dashboard
![Student Dashboard](https://github.com/user-attachments/assets/3a97d135-b165-49ac-8364-85720faa9518)



---

## ✨ Features

## 👨‍🎓 Students

### 🌟 Features:
- ✅ **Sign Up & Login**: Create a secure account to begin learning.
  ![image](https://github.com/user-attachments/assets/91769421-4321-4a89-b9c0-284743f35a3e)
![image](https://github.com/user-attachments/assets/bd439629-0b7a-4694-b0ba-19d958139447)

- 📚 **View Courses**: Browse and enroll in a variety of sign language-supported courses.
  ![image](https://github.com/user-attachments/assets/d569b0d2-ba12-4af7-be2c-ffafe67c09dd)

- 🎥 **Watch Lectures**: Learn using visual sign language videos and simple language.
  ![image](https://github.com/user-attachments/assets/ef016a9d-d545-4301-bc30-1bc4b142394c)

- 📝 **Take Quizzes**: Reinforce learning with engaging, child-friendly MCQs.
  ![image](https://github.com/user-attachments/assets/a6cad840-f30d-4641-926e-7c18b5b6c42c)

- 📊 **Track Progress**: See completed lectures and quiz scores.
  ![image](https://github.com/user-attachments/assets/a23bd052-4901-4817-b6ae-1fbc7664345b)

- 🏆 **Earn Certificates**: Receive a certificate upon course completion.
- 📂 **Accessible Content**: Lessons are tailored for children using easy words and concepts.

---

## 👩‍🏫 Teachers

### 🌟 Features:
- ✅ **Sign Up & Login**: Secure access to the teacher dashboard.
- ➕ **Add Courses**: Create new sign language-supported courses with titles and descriptions.
- 🎬 **Upload Lectures**: Add video lessons with simplified educational content.
- ❓ **Create Quizzes**: Design custom quizzes with multiple-choice questions.
- 📈 **View Student Submissions**: Check quiz participation and student understanding.
- ✏️ **Update or Delete Content**: Manage course content with full control.

---

## 👨‍💼 Admins

### 🌟 Features:
- ✅ **Secure Admin Login**
- 📊 **Dashboard Overview**:
  - Total Students
  - Total Courses
  - Total Lectures
  - Total Quizzes
- ➕ **Add Courses & Lectures**: Full control to manage educational content.
- 📁 **Manage Users**: View, update, or remove student and teacher accounts.
- 🔒 **Content Moderation**: Ensure all uploaded material is appropriate and accessible.
- 📬 **Monitor Platform Activity**: Oversee learning engagement, quiz results, and course progress.

---

## 📚 Available Courses

### 1. 🇵🇰 National Anthem of Pakistan  
- **Learn the meaning and message of the national anthem with sign support.**
- Includes a 5-question quiz with child-friendly options.

### 2. 🇬🇧 English for Kids – Learn with Signs  
- **Learn English basics with engaging stories, vocabulary, grammar, and more.**
- 10 Lectures: From alphabets, body parts, and vowels to stories and grammar.
- Includes a 10-question quiz.

### 3. 💻 Computer Basics – A Beginner’s Guide to the Digital World  
- **Start your digital journey with simple lessons on computers, emails, internet, and more.**
- 9 Lectures: From MS Office and internet safety to chatbots and smartphones.
- Includes a 10-question quiz.

---



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
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Set Up MongoDB
Create a MongoDB Atlas account and set your connection string in app.py:
```python
client = MongoClient("your_mongodb_uri")
```
### 5. Run the App
```bash
python app.py
```
Then open http://localhost:5000 in your browser.

---
## 🧠 Future Enhancements

- 🎥 **Live video signing practice** via webcam  
- 🌍 **Multilingual sign language support** (e.g., ASL, BSL)  
- 🤖 **AI sign recognition** using OpenCV & MediaPipe  
- 🏆 **Gamification features** such as badges and leaderboards  
---

## 🙌 Contributing

We welcome community contributions to **GESTEROIC** and overall platform improvement!  
Feel free to **fork the repo** and **raise a pull request** 🚀

---

## 🧾 License

This project is licensed under the **MIT License**.

---

## 🧑‍🎓 Credits

- **Aymen** – Developer & Designer  
- **PUCIT** – Final Year Project Support  
- **OpenAI & DeepLearning.AI** – Prompt Engineering, LangChain Skills  
- **MongoDB Atlas** – Cloud Database Hosting  
- **YouTube** – Video Hosting for Lectures  

---

## 📬 Contact

- 📧 **Email:** ayemenbaig26@gmail.com  
- 🌐 **LinkedIn:** [LinkedIn Profile](https://www.linkedin.com/) 

