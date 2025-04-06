
import os
import json
import pyttsx3
import speech_recognition as sr
from fpdf import FPDF

# ================== DATA HANDLING + PARSER ===================
def simulate_llm_parser(monologue):
    parsed = {
        "name": "Not provided",
        "tag": "Not provided",
        "location": "Not provided",
        "education": "Not provided",
        "experience": [],
        "projects": [],
        "email": "Not provided",
        "skills": [],
        "interests": []
    }

    if "backend" in monologue.lower():
        parsed["tag"] = "Backend Engineer"
        parsed["skills"] = ["Python", "APIs", "Databases"]

    if "tcs" in monologue.lower():
        parsed["experience"].append({
            "company": "TCS",
            "role": "Software Intern",
            "duration": "6 months",
            "bullets": [
                "Built internal HR tool",
                "Improved dashboard performance"
            ]
        })

    if "resume" in monologue.lower():
        parsed["projects"].append({
            "title": "BlindCVBuilder",
            "description": "Voice-based resume builder for blind users"
        })

    if "koch" in monologue.lower():
        parsed["location"] = "Kochi"

    if "n i t" in monologue.lower():
        parsed["education"] = "B.Tech in Computer Science from NIT Calicut"

    if "alenso" in monologue.lower():
        parsed["name"] = "Alenso"

    return parsed

# ================== VOICE HELPERS ===================
engine = pyttsx3.init()
engine.setProperty('rate', 175)

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def speech_to_text_continuous():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening... Speak freely, it will stop once you pause.")
        audio = recognizer.listen(source, timeout=None)
        try:
            response = recognizer.recognize_google(audio)
            print("Captured:", response)
            return response
        except Exception as e:
            print("STT Error:", e)
            return None

# ================== PROMPT FILLER ===================
REQUIRED_FIELDS = ["name", "tag", "location", "education", "experience", "projects", "email"]
QUESTION_BANK = {
    "name": "What is your full name?",
    "tag": "What is your profession or role?",
    "location": "Where are you currently based?",
    "education": "What is your latest qualification and where did you study?",
    "experience": "Can you briefly describe your work or internship experience?",
    "projects": "Tell me about a project you've worked on.",
    "email": "What is your email address?"
}

def ai_prompt_filler(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    updated = False
    for field in REQUIRED_FIELDS:
        if field not in data or not data[field]:
            question = QUESTION_BANK.get(field)
            if question:
                text_to_speech(question)
                answer = speech_to_text_continuous()
                if answer:
                    if field in ["experience", "projects"] and isinstance(data.get(field), list):
                        if field == "experience":
                            data[field].append({
                                "company": "User Provided",
                                "role": "Not specified",
                                "duration": "Not specified",
                                "bullets": [answer]
                            })
                        else:
                            data[field].append({
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

# ================== PDF CREATOR ===================
class MinimalistResumePDF(FPDF):
    def header(self):
        self.set_font("Times", 'B', 20)
        self.cell(0, 10, data.get("name", "Your Name").upper(), ln=True, align="C")
        self.set_font("Times", size=11)
        contact_line = f"{data.get('location', '')} | {data.get('email', '')} | linkedin.com/in/testuser | github.com/testuser"
        self.cell(0, 8, contact_line, ln=True, align="C")
        self.ln(3)

    def section_title(self, title):
        self.set_font("Times", 'B', 13)
        self.cell(0, 8, title.upper(), ln=True)
        self.set_draw_color(150)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)

    def bullet_section(self, lines):
        self.set_font("Times", size=11)
        for line in lines:
            self.multi_cell(0, 6, f"- {line}")
        self.ln(2)

    def experience_block(self, role, company, duration, bullets):
        self.set_font("Times", 'B', 12)
        self.cell(0, 7, f"{company}", ln=True)
        self.set_font("Times", 'I', 11)
        self.cell(0, 6, f"{role} | {duration}", ln=True)
        self.bullet_section(bullets)

    def project_block(self, title, description):
        self.set_font("Times", 'B', 12)
        self.cell(0, 7, title, ln=True)
        self.set_font("Times", size=11)
        self.multi_cell(0, 6, description)
        self.ln(1)

    def two_column_list(self, label, items):
        self.set_font("Times", 'B', 11)
        self.cell(0, 6, f"{label}:", ln=True)
        self.set_font("Times", size=11)
        half = (len(items) + 1) // 2
        col1 = items[:half]
        col2 = items[half:]
        max_len = max(len(col1), len(col2))
        for i in range(max_len):
            line = ""
            if i < len(col1):
                line += f"{col1[i]:<40}"
            else:
                line += " " * 40
            if i < len(col2):
                line += f"{col2[i]}"
            self.cell(0, 6, line, ln=True)
        self.ln(1)

def generate_pdf_from_json(json_file, output_pdf):
    global data
    with open(json_file) as f:
        data = json.load(f)
    pdf = MinimalistResumePDF()
    pdf.set_auto_page_break(auto=False, margin=10)
    pdf.add_page()

    pdf.section_title("Education")
    pdf.multi_cell(0, 6, data.get("education", "Not provided"))
    pdf.ln(2)

    if data.get("experience"):
        pdf.section_title("Experience")
        for exp in data["experience"]:
            pdf.experience_block(exp["role"], exp["company"], exp["duration"], exp["bullets"])

    if data.get("projects"):
        pdf.section_title("Projects")
        for proj in data["projects"]:
            pdf.project_block(proj["title"], proj["description"])

    if data.get("skills"):
        pdf.section_title("Technical Skills")
        pdf.two_column_list("Skills", data["skills"])

    if data.get("interests"):
        pdf.section_title("Interests")
        pdf.two_column_list("Areas of Interest", data["interests"])

    pdf.output(output_pdf)

# ================== MAIN FLOW ===================
def main():
    text_to_speech("Please introduce yourself. Start speaking now.")
    monologue = speech_to_text_continuous()
    if not monologue:
        text_to_speech("Sorry, I didn't catch that.")
        return

    parsed = simulate_llm_parser(monologue)
    json_file = "parsed_monologue_cv.json"
    with open(json_file, "w") as f:
        json.dump(parsed, f, indent=4)

    ai_prompt_filler(json_file)

    final_pdf = "AI_Resume_Final_Auto.pdf"
    generate_pdf_from_json(json_file, final_pdf)
    text_to_speech("Your resume has been created and saved successfully.")

if __name__ == "__main__":
    main()
