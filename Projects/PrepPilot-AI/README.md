# 🎯 AceKTU

**AI-powered study assistant built specifically for KTU (APJ Abdul Kalam Technological University) students under the 2024 curriculum scheme.**

## The Problem

KTU introduced a new academic scheme in 2024 — modules dropped from 5 to 4, total exam marks changed from 100 to 60, and the Part A/B marking pattern shifted. This means thousands of students have almost no past-year question papers that match the new pattern, making exam prep guesswork.

## What AceKTU Does

1. **Upload your study materials** — one or more PDFs/PowerPoint files, even if you only have notes for some modules
2. **Enter your subject code and exam date**
3. AceKTU researches the official 2024-scheme syllabus, cross-references available past papers, and combines it with your own notes
4. **Get a personalized study map**: a day-by-day study schedule, modules ranked by ease of mastery, key points with explanations, likely exam questions with full model answers, and a downloadable quick-revision PDF

## Features

- 📄 Multi-file upload (PDF + PowerPoint support)
- 🔍 AI-powered subject research with Google Search grounding, cached per subject to avoid redundant lookups
- 📅 Exam-date-aware day-by-day study scheduling
- ✅ Interactive module completion tracking with live progress rings
- 💻 Auto-formatted code snippets for programming subjects
- 🖼️ Diagram reference links for questions requiring visual answers
- 📥 One-click quick-revision PDF export
- ⚠️ Accurate 2024-scheme marking pattern verification (fixes common AI confusion between old/new schemes)
- 🚫 Invalid subject code detection

## Tech Stack

- **Frontend:** Streamlit
- **AI:** Google Gemini API (gemini-2.5-flash) with Google Search grounding
- **PDF Processing:** PyPDF2
- **PowerPoint Processing:** python-pptx
- **PDF Generation:** fpdf2
- **Visualization:** Plotly
- **Deployment:** Streamlit Community Cloud

## Live Demo

🔗 [Try AceKTU here](your-deployed-link-here)

## Screenshots

*(add screenshots here)*

## Running Locally

If you'd like to run this project on your own machine:

**1. Clone the repository:**
```bash
git clone https://github.com/FazilFirose/AceKTU.git
cd AceKTU
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Get your own free Gemini API key:**
- Go to [aistudio.google.com](https://aistudio.google.com)
- Sign in with Google, accept the terms
- Click "Get API key" → "Create API key"

**4. Create a `.env` file in the project root** (this file is gitignored and stays private to you) with:`GEMINI_API_KEY=your_key_here`

**5. Run the app:**
```bash
streamlit run app.py
```

## Built By

Fazil Firose Ibrahim — [LinkedIn](www.linkedin.com/in/fazil-firose-ibrahim-97a378255) | [GitHub](https://github.com/FazilFirose)