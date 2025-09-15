---The AI Education Mentor: Enhancing Student Retention with NLP--- 

(1) --->Project Overview  
This project aims to reduce **student dropout rates** by providing an **AI-powered Education Mentor** that uses **Natural Language Processing (NLP)**.  
It integrates:  
- A **faculty & student management system**  
- A **learning dashboard** for sharing materials  
- An **AI Chatbot** built in Python, connected to the web app via Flask API  



--->Features  
- 🔑 Faculty Registration & Login(HTML, Node.js, MongoDB)  
- 📝 Marks Entry Portal – Faculty can enter class/group-wise marks  
- 👩‍🎓 Student Login– Students can log in with roll number & DOB  
- 📊 Dashboard – Teachers upload study materials for students  
- 🤖 AI Chatbot – Provides academic mentoring & support (Flask + NLP)  



--->Tech Stack  
- Frontend: HTML, CSS, JavaScript  
- Backend: Node.js, Express.js  
- Database: MongoDB  
- Chatbot: Python (Flask, NLP model)  
- Other: EJS templates for rendering student profiles  



---> Folder Structure  
│── Aboutpage.html
│── Facultylogin.html
│── Facultyregisteration.html
│── Facultyregistration.js
│── Facultyregister.js
│── HomePage.html
│── Mark.html
│── markscript.js
│── Studentlogin.html
│── Studentlogin.js
│── dashboard.html
│── learning.html
│── form.html
│── syllabus.html
│── chatbot_model.h5
│── words.py
│── classes.py
│── bot.py # Main entry point (Flask chatbot + app runner)
│── server.js # Node + Express server
│── package.json # Node dependencies
│── package-lock.json
│── requirements.txt # Python dependencies (Flask, nltk, pymongo, etc.)
│── /templates # HTML/EJS templates
│── /node_modules





---> Installation & Setup  

Clone the repository  
```bash
git clone https://github.com/Akthar24/AI-Education-Mentor.git
cd AI-Education-Mentor

(2) Install Node.js dependencies 

npm install

(3) Install Python dependencies

pip install -r requirements.txt

(4) Run the application

Open a terminal in the project folder and run:
python bot.py

This will start the chatbot and web application.
-----> Visit the link shown in the terminal (usually http://localhost:5000).

---> Future Enhancements

1.Predict dropout risks with AI models.

2.Smarter AI chatbot for personalized guidance.

3.Admin dashboard with analytics.

