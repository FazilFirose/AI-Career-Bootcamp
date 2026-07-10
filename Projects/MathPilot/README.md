# 🧠 MathPilot AI

MathPilot AI is a desktop-based AI mathematics assistant built with Python. It combines AI-powered natural language understanding, symbolic mathematics, and voice interaction to solve mathematical problems through both text and speech.

---

## ✨ Features

- 🤖 AI-powered mathematical interpretation using Groq
- ➕ Solves algebra, calculus, trigonometry, logarithms, and more
- 🎤 Voice input with wake word activation ("Hey Math")
- 🔊 Text-to-Speech responses
- ⌨️ Text input support
- 🧮 Symbolic computation using SymPy
- 🌙 Modern dark-themed desktop interface
- ⚡ Fast response time

---

## 📸 Screenshots

> Add screenshots inside a `screenshots/` folder.

### Main Interface

![Main UI](screenshots/main_ui.png)

### Solving a Question

![Solve](screenshots/solve_example.png)

### Voice Mode

![Voice](screenshots/voice_mode.png)

---

## 🛠 Technologies Used

- Python 3.13
- CustomTkinter
- Groq API
- SymPy
- SpeechRecognition
- Faster Whisper
- Edge-TTS
- pygame
- python-dotenv

---

## 📂 Project Structure

```text
MathPilot/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── ai/
│   ├── groq_client.py
│   ├── interpreter.py
│   └── prompts.py
│
├── solver/
│   └── sympy_solver.py
│
├── voice/
│   ├── speech.py
│   ├── tts.py
│   ├── wakeword.py
│   └── voice_controller.py
│
├── gui/
│   ├── theme.py
│   ├── widgets.py
│   └── main_window.py
│
└── assets/
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/MathPilot.git
```

Move into the project

```bash
cd MathPilot
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```text
GROQ_API_KEY=your_api_key_here
```

Run the application

```bash
python app.py
```

---

## 🎤 Voice Commands

Wake the assistant by saying:

```
Hey Math
```

Example questions:

- What is 25 factorial?
- Differentiate x² + 5x
- Integrate sin(x)
- Solve x² − 5x + 6 = 0
- Expand (550 + 650)²

---

## 🧠 How It Works

```text
Voice / Text
      │
      ▼
Groq AI
      │
Natural Language Interpretation
      │
      ▼
SymPy Solver
      │
      ▼
Formatted Answer
      │
      ▼
GUI + Voice Output
```

---

## 📌 Current Capabilities

- Natural language math understanding
- Symbolic mathematics
- Voice interaction
- Wake word activation
- Speech output
- Desktop GUI

---

## 🔮 Future Improvements

- Image OCR for handwritten equations
- Mathematical graph plotting
- Step-by-step solutions
- Conversation history
- Cross-platform executable

---

## 👨‍💻 Author

**Fazil Firose Ibrahim**

B.Tech in Computer Science (Data Science)

Interested in:

- Artificial Intelligence
- Python Development
- Machine Learning
- Automation
- Desktop Applications

GitHub: https://github.com/FazilFirose


---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.