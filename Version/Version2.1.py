
# BlindCVBuilder Combined Script - v1.0
# All modules merged: TTS, STT, retry, confirmation, smart flow, QR, style, email

import os
import json
import pyttsx3
import speech_recognition as sr
from fpdf import FPDF
import qrcode
from datetime import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

QUESTIONS = {
    "name": "What is your full name?",
    "date_of_birth": "What is your date of birth? (Please provide in DD/MM/YYYY format)",
    "country": "Which country do you currently live in?",
    "city": "Which city do you currently live in?",
    "phone": "What is your phone number, including the country code?",
    "email": "What is your email address?",
    "github": "Do you have a GitHub profile or portfolio link you’d like to include?",
    "tag": "What do you do for a living?",
    "linkedin": "Do you have a LinkedIn profile you’d like to share?",
    "education": "What is your highest degree and the name of your university/college?",
    "school": "Which school did you attend for your XII (12th grade)?",
    "experience": "Have you had any internships or job experiences? If yes, mention your position, company, and duration.",
    "responsibilities": "Have you held any leadership positions in college, clubs, or organizations? Please describe.",
    "projects": "Have you worked on any academic or personal projects? Provide the title and a brief description.",
    "achievements": "Have you received any certifications or participated in any competitions? If yes, please specify.",
    "qr_code": "Would you like to include a QR code linking to your LinkedIn profile? (Yes/No)",
    "style": "Which CV style do you prefer? Say 'Basic' or 'Highlight'."
}

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
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
    except Exception as e:
        print(f"STT Error: {e}")
        return None

def send_email(receiver_email, attachment_path):
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"
    subject = "Your CV from BlindCVBuilder"
    body = "Hello! Attached is the CV you just created."

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with open(attachment_path, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        text_to_speech("Your CV has been emailed successfully.")
    except Exception as e:
        print(f"Email failed: {e}")
        text_to_speech("I was unable to send the email.")

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
        if self.style == "highlight":
            self.set_fill_color(220, 240, 255)
            self.set_text_color(0, 0, 120)
            self.cell(0, 10, title, ln=True, fill=True)
            self.set_text_color(0, 0, 0)
        else:
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

    recipient_email = data.get("email")
    if recipient_email and "@" in recipient_email:
        send_email(recipient_email, output_pdf)

def collect_responses():
    responses = {}
    for key, question in QUESTIONS.items():
        confirmed = False
        while not confirmed:
            text_to_speech(question)
            response = speech_to_text()
            if response:
                cmd = response.lower()
                if "skip" in cmd:
                    text_to_speech("Skipping this question.")
                    responses[key] = "Skipped by user"
                    break
                if "repeat" in cmd:
                    text_to_speech("Repeating the question.")
                    continue
                if "pause" in cmd:
                    text_to_speech("Pausing for a few seconds.")
                    time.sleep(5)
                    continue

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
