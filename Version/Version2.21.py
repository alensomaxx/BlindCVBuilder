
import os
import json
import pyttsx3
import speech_recognition as sr
from fpdf import FPDF
import qrcode
from datetime import datetime
import time

#version2.21

# Setup TTS
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

def text_to_speech(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

def speech_to_text():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)
            return recognizer.recognize_google(audio)
    except Exception as e:
        print(f"STT Error: {e}")
        return None

class PDF(FPDF):
    def __init__(self, style="basic"):
        super().__init__()
        self.style = style.lower()

    def header(self):
        with open("current_user.json") as f:
            data = json.load(f)
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, data.get("name", "Your Name"), ln=True, align="C")
        self.set_font("Arial", 'I', 10)
        self.cell(0, 8, data.get("tag", "Your Tagline"), ln=True, align="C")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def section_title(self, title):
        self.set_font("Arial", 'B', 13)
        self.cell(0, 10, title, ln=True)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def section_content(self, content):
        self.set_font("Arial", size=11)
        for line in content.split(". "):
            self.multi_cell(0, 8, f"- {line.strip()}")
        self.ln(2)

    def add_hyperlink(self, label, url):
        self.set_text_color(0, 0, 255)
        self.set_font("Arial", 'U', 11)
        self.cell(0, 8, f"{label}: {url}", ln=True, link=url)
        self.set_text_color(0, 0, 0)

    def add_qr_code(self, url, filename):
        qr = qrcode.make(url)
        qr.save(filename)
        self.image(filename, x=160, y=self.get_y() + 10, w=30)
        os.remove(filename)

def create_cv(json_file, output_pdf):
    with open(json_file) as f:
        data = json.load(f)
    pdf = PDF(style=data.get("style", "basic"))
    pdf.add_page()

    for section in ["education", "experience", "projects", "responsibilities", "achievements"]:
        pdf.section_title(section.replace("_", " ").upper())
        pdf.section_content(data.get(section, "Not provided"))

    pdf.section_title("CONTACT")
    for label in ["email", "github", "linkedin"]:
        val = data.get(label)
        if val and val.lower() != "not provided":
            pdf.add_hyperlink(label.capitalize(), val)
            if label == "linkedin" and data.get("qr_code", "").lower() == "yes":
                pdf.add_qr_code(val, "linkedin_qr.png")

    pdf.output(output_pdf)
    text_to_speech("Your CV has been created successfully.")

def collect_responses():
    responses = {}

    # ASK ONLY 2 QUESTIONS
    for key, question in {
        "name": "What is your full name?",
        "tag": "What do you do for a living?"
    }.items():
        confirmed = False
        while not confirmed:
            text_to_speech(question)
            response = speech_to_text()
            if response:
                confirm = f"You said: {response}. Should I save this? Say Yes or No."
                text_to_speech(confirm)
                conf = speech_to_text()
                if conf and "yes" in conf.lower():
                    responses[key] = response
                    confirmed = True
                else:
                    text_to_speech("Okay, let's try again.")
            else:
                text_to_speech("I didn't catch that. Please try again.")

    # Fill mock data for all other fields
    responses.update({
        "date_of_birth": "01/01/2000",
        "country": "India",
        "city": "Kochi",
        "phone": "+91XXXXXXXXXX",
        "email": "test@example.com",
        "github": "https://github.com/testuser",
        "linkedin": "https://linkedin.com/in/testuser",
        "education": "B.Tech in Computer Science from XYZ University",
        "school": "ABC School",
        "experience": "Software Intern at TestCorp for 6 months",
        "responsibilities": "Class Representative and Media Club Head",
        "projects": "Voice Controlled CV Builder using Python",
        "achievements": "Winner at Inter-College Coding Contest",
        "qr_code": "yes",
        "style": "basic"
    })

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = f"responses_{timestamp}.json"
    pdf_file = f"cv_{timestamp}.pdf"

    with open("current_user.json", "w") as f:
        json.dump(responses, f, indent=4)
    with open(json_file, "w") as f:
        json.dump(responses, f, indent=4)

    text_to_speech("All responses recorded. Generating your CV.")
    create_cv(json_file, pdf_file)

if __name__ == "__main__":
    collect_responses()
