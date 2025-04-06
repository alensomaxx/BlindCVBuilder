# 🧠 BlindCVBuilder — Voice-Powered Resume Builder

BlindCVBuilder is an assistive Python tool designed to help **visually impaired users** create a professional CV **using only their voice**.

🎙️ The user speaks their answers.  
📄 The app builds a clean PDF resume.  
📤 It even sends it to their email.  

This version is trying to optimize for **speed, low latency**, and currently asks **just two questions for testing purposes**.

---

## 📌 Project Vision

Our goal is to create a voice-first experience for blind or visually impaired individuals to:
- Build a resume without ever needing a keyboard
- Get audio feedback at every step
- Export and email a beautiful PDF CV
- Eventually support multiple languages, templates, and even job application workflows

BlindCVBuilder aims to democratize professional documentation with **inclusive technology**.

---

## 🎯 Core Features (as of v1.0 Test Release)

| Feature                           | Description |
|----------------------------------|-------------|
| 🎤 Voice-Driven Input             | User answers via microphone |
| 🔁 Retry & Confirmation Flow     | App confirms each answer and allows corrections |
| 🔊 Offline Text-to-Speech (TTS)  | pyttsx3 ensures fast, local speech |
| 📈 Fast Voice Recognition        | Uses Google’s STT with low timeout to minimize lag |
| 📄 PDF Resume Generation         | Uses FPDF to build a polished, sectioned CV |
| 🔗 Clickable Hyperlinks          | GitHub, Email, LinkedIn shown as links |
| 📷 QR Code for LinkedIn          | Automatically added if user wants it |
| 🧾 JSON Response Logging         | Stores each session uniquely with timestamp |
| 💡 Template Style Choice         | Basic & Highlight modes available |
| ⚡ Light Testing Mode (2 questions) | Ideal for debugging + performance testing |

---

## 🚀 How to Run (Test Mode)

### 1. Clone or Download this Repo

### 2. Install dependencies:
```bash
pip install pyttsx3 speechrecognition fpdf qrcode
```

### 3. Run the test version:
```bash
python Version2.21.py
```

> 🎙️ The app will ask 2 questions (Name and Profession).  
> It fills in mock data for the rest.  
> Outputs a clean PDF resume in the same folder.

---

## 🧪 What’s Being Used (Tech Stack)

- `pyttsx3`: Offline Text-to-Speech
- `speech_recognition`: Voice-to-Text via Google
- `FPDF`: Resume generation
- `qrcode`: QR code embedding for LinkedIn
- `json`: Response logging
- `datetime`: Timestamped file naming

---

## 🧱 Current Folder Output

| File | Description |
|------|-------------|
| `responses_YYYYMMDD_HHMMSS.json` | JSON of user answers |
| `cv_YYYYMMDD_HHMMSS.pdf`         | The final resume |
| `current_user.json`              | Used for PDF generation headers |

---

## 🌍 Vision — Endless Possibilities

Imagine what's next:

- 🌐 **Web version**: Built with Streamlit or Flask for accessibility
- 🗣️ **Multi-language voice support**
- 🧩 **Template switcher with preview**
- 📤 **CV auto-emailing after generation**
- 🧠 **Auto-formatting & grammar fixes**
- 📄 **PDF + DOCX export formats**
- 🤝 **Job portal integration** for blind-friendly career support
- 📱 **Mobile version with voice assistant integration**

---

## 🔮 Roadmap: Upcoming Updates

| Update | Description |
|--------|-------------|
| ✅ Add retry/confirmation | Already implemented |
| ✅ Voice-command support (skip, repeat, pause) | Done |
| ✅ Fast test-mode setup | Done |
| ⏳ Full flow mode (all questions) | Coming |
| ⏳ Custom section ordering | Coming |
| ⏳ Email sending (SMTP) | Coming back soon |
| ⏳ Style preview mode | Under construction |
| ⏳ Save/edit multiple versions | On roadmap |
| ⏳ Accessibility audit | Planned |

---

## 🧑‍💻 Author

**ALENSO**  
GitHub: [@alensomaxx](https://github.com/alensomaxx)

---

## 📄 License

This project is licensed under the **MIT License**

---

> This tool is for everyone who dreams, learns, applies, and grows — no matter what challenges they face. Let’s build tech that belongs to **all of us**.
