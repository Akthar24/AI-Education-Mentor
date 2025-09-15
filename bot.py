import nltk
import numpy as np
import json
import re
from tensorflow.keras.models import load_model
from flask import Flask, request, render_template, redirect, url_for, jsonify
from nltk.stem import WordNetLemmatizer
from threading import Thread
import pyttsx3
import random
import speech_recognition as sr
import os
from flask import send_file
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
from bson.objectid import ObjectId
import bcrypt


# Download NLTK data
#nltk.download('wordnet')
#nltk.download('punkt')

# Initialize Flask app

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/students"
mongo = PyMongo(app)
# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize Lemmatizer
lemmatizer = WordNetLemmatizer()

# Load chatbot intents
def load_intents():
    with open('bot.json', 'r', encoding='utf-8') as file:
        return json.load(file)

# Prepare training data
def prepare_data(intents):
    words = []
    classes = []
    documents = []

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            word_list = nltk.word_tokenize(pattern)
            words.extend(word_list)
            documents.append((word_list, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    words = [lemmatizer.lemmatize(w.lower()) for w in words if w.isalpha()]
    words = sorted(set(words))
    classes = sorted(set(classes))

    training = []
    output_empty = [0] * len(classes)

    for doc in documents:
        bag = []
        pattern_words = [lemmatizer.lemmatize(word.lower()) for word in doc[0]]
        
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training, dtype=object)

    train_x = np.array(list(training[:, 0]))
    train_y = np.array(list(training[:, 1]))

    return train_x, train_y, words, classes

# Load intents and model
intents = load_intents()
train_x, train_y, words, classes = prepare_data(intents)
model = load_model('chatbot_model1.h5')

# Clean input text
def clean_input(user_input):
    cleaned_input = re.sub(r'[^\w\s,.]', '', user_input.lower())
    cleaned_input = re.sub(r'\s+', ' ', cleaned_input).strip()
    return cleaned_input

# Split user input into queries
def split_queries(user_input):
    queries = re.split(r',\s*|\.\s*|\s+and\s+|\s+or\s+', user_input)
    return [query.strip() for query in queries if query.strip()]

# Split concatenated words based on known words
def split_concatenated_words(input_str, words):
    split_result = []
    current_str = input_str.lower()

    while current_str:
        found = False
        for word in sorted(words, key=len, reverse=True):
            if current_str.startswith(word):
                split_result.append(word)
                current_str = current_str[len(word):]
                found = True
                break
        if not found:
            split_result.append(current_str)
            break
    return split_result

# Process user input
def process_input(user_input):
    cleaned_input = clean_input(user_input)
    if " " not in cleaned_input:
        words_split = split_concatenated_words(cleaned_input, words)
        processed_input = " ".join(words_split)
    else:
        processed_input = cleaned_input
    return processed_input

# Generate chatbot response
def chatbot_response(msg):
    unknown_responses = [
        "I'm sorry, I couldn't understand that. Could you please rephrase?",
        "I didn't get that. Can you please ask the question more specifically?"
    ]

    single_response_tags = ["greeting", "goodbye", "hi", "hello", "bye", "see you later"]

    processed_msg = process_input(msg)
    queries = split_queries(processed_msg)

    responses = []
    understood_any = False

    for query in queries:
        used_single_response = False
        bag = [0] * len(words)
        input_words = nltk.word_tokenize(query)
        input_words = [lemmatizer.lemmatize(w.lower()) for w in input_words]

        for w in input_words:
            if w in words:
                bag[words.index(w)] = 1
        res = np.array([bag])

        # Predict intents using the loaded model
        results = model.predict(res)[0]
        confidence_threshold = 0.7
        detected_tags = [i for i, prob in enumerate(results) if prob > confidence_threshold]

        if detected_tags:
            understood_any = True
            for tag_index in detected_tags:
                tag = classes[tag_index]

                if tag in single_response_tags and not used_single_response:
                    for i in intents['intents']:
                        if i['tag'] == tag:
                            responses.append(random.choice(i['responses']))
                    used_single_response = True
                elif tag not in single_response_tags:
                    for i in intents['intents']:
                        if i['tag'] == tag:
                            responses.append(random.choice(i['responses']))

    if not understood_any:
        responses.append(random.choice(unknown_responses))

    return "\n".join(responses)

# Route for Homepage

# Ensure correct file paths
BASE_DIR = r"C:/Users/barve/OneDrive/Desktop/Miniproject.html"

@app.route("/")
def dashboard():
    return send_file(os.path.join(BASE_DIR, "dashboard.html"))

@app.route("/school_image")
def school_image():
    return send_file(os.path.join(BASE_DIR, "Schoolimg.png"))

@app.route("/home")
def homepage():
    return send_file(os.path.join(BASE_DIR, "Homepage.html"))

@app.route("/about")
def about():
    return send_file(os.path.join(BASE_DIR, "Aboutpage.html"))

@app.route("/gallery")
def gallery():
    return "<h1>Gallery is currently under development!</h1>"

@app.route("/student_corner")
def student_corner():
    return send_file(os.path.join(BASE_DIR, "studentlogin.html"))

@app.route("/faculty_login", methods=["GET", "POST"])
def faculty_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        faculty = mongo.db.Faculty.find_one({"email": email})

        if not faculty:
            return "Faculty not found. Please register first.", 404

        if not bcrypt.checkpw(password.encode('utf-8'), faculty["password"].encode('utf-8')):
            return "Invalid email or password.", 401

        return redirect(url_for("mark_page"))

    # Use send_file to serve Facultylogin.html
    return send_file(os.path.join(BASE_DIR, "Facultylogin.html"))

@app.route("/faculty_register", methods=["GET", "POST"])
def faculty_register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return "Passwords do not match.", 400

        existing_faculty = mongo.db.Faculty.find_one({"email": email})
        if existing_faculty:
            return "Faculty already registered with this email.", 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        mongo.db.faculty.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password.decode('utf-8')
        })

        return redirect(url_for("faculty_login"))

    # Use send_file to serve Facultyregistration.html
    return send_file(os.path.join(BASE_DIR, "Facultyregistration.html"))


@app.route("/mark")
def mark_page():
    return send_file(os.path.join(BASE_DIR, "mark.html"))

@app.route("/faculty_corner")
def faculty_corner():
    return redirect(url_for("faculty_login"))


@app.route("/schemes")
def schemes():
    return send_file(os.path.join(BASE_DIR, "Schemes.html"))

@app.route("/risk_analysis")
def risk_analysis():
    return send_file(os.path.join(BASE_DIR, "Risk.html"))

@app.route("/syllabus")
def syllabus():
    return send_file(os.path.join(BASE_DIR, "Syllabus.html"))

@app.route("/help_desk")
def help_desk():
    return send_file(os.path.join(BASE_DIR, "templates/ind.html"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        roll_no = request.form.get("roll_no")
        dob = request.form.get("dob")

        if not roll_no or not dob:
            return "Roll number and date of birth are required.", 400

        student = mongo.db.users.find_one({
            "roll_no": roll_no,
            "dob": datetime.strptime(dob, '%Y-%m-%d')
        })

        if not student:
            return "Student not found or incorrect login details.", 404

        return render_template("student_profile.html", student=student)

    return render_template("studentlogin.html")

@app.route("/student_profile")
def student_profile():
    return render_template("student_profile.html")

# Handle chatbot responses
@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.json
    user_input = data.get("message")
    is_voice_query = data.get("isVoiceQuery", False)

    if is_voice_query:
        user_input = speech_to_text()

    response = chatbot_response(user_input)

    if is_voice_query:
        thread = Thread(target=speak, args=(response,))
        thread.start()

    return jsonify({"response": response})

# Text-to-speech function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your query...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat?")
            return "Sorry, I didn't catch that. Could you please repeat?"
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
            return "Sorry, there was an issue with the speech recognition service."

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True, port=5000)
