
import os
import json
import pyttsx3
import speech_recognition as sr
import keyboard
import time

engine = pyttsx3.init()
engine.setProperty('rate', 175)

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def push_to_talk_record():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Hold SPACEBAR to start talking...")
        text_to_speech("Hold the spacebar to start speaking.")
        while True:
            if keyboard.is_pressed("space"):
                print("🎙️ Recording... release spacebar to finish.")
                audio = recognizer.listen(source, phrase_time_limit=None)
                print("🛑 Spacebar released. Processing...")
                break
        try:
            transcript = recognizer.recognize_google(audio)
            print("You said:", transcript)
            return transcript
        except Exception as e:
            print("Error:", e)
            return None

# Simple test function
def main():
    text_to_speech("This is a test of push to talk. Please press and hold the spacebar while speaking.")
    transcript = push_to_talk_record()
    if transcript:
        text_to_speech("Thank you. I heard you say:")
        text_to_speech(transcript)
    else:
        text_to_speech("Sorry, I couldn't understand what you said.")

if __name__ == "__main__":
    main()
