
import json
import pyttsx3
import speech_recognition as sr
import time

# Setup TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening for answer...")
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
        try:
            response = recognizer.recognize_google(audio)
            print("User said:", response)
            return response
        except Exception as e:
            print("STT Error:", e)
            return None

# Define required top-level fields
REQUIRED_FIELDS = [
    "name", "tag", "location", "education", "experience",
    "projects", "email"
]

# Questions to ask for missing fields
QUESTION_BANK = {
    "name": "What is your full name?",
    "tag": "What is your profession or role?",
    "location": "Where are you currently based?",
    "education": "What is your latest qualification and where did you study?",
    "experience": "Can you briefly describe your work or internship experience?",
    "projects": "Tell me about a project you've worked on.",
    "email": "What is your email address?"
}

# Load JSON, prompt for missing fields, and update
def ai_prompt_filler(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    updated = False
    for field in REQUIRED_FIELDS:
        if field not in data or not data[field]:
            question = QUESTION_BANK.get(field)
            if question:
                text_to_speech(question)
                answer = speech_to_text()
                if answer:
                    if field in ["experience", "projects"] and isinstance(data.get(field), list):
                        # Append structured entry
                        data[field].append({
                            "company": "User Provided",
                            "role": "Not specified",
                            "duration": "Not specified",
                            "bullets": [answer]
                        }) if field == "experience" else data[field].append({
                            "title": "User Project",
                            "description": answer
                        })
                    else:
                        data[field] = answer
                    updated = True

    if updated:
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)
        print("✅ Updated JSON with new responses.")
        text_to_speech("Thanks! I've added your responses.")

if __name__ == "__main__":
    ai_prompt_filler("parsed_monologue_cv.json")
