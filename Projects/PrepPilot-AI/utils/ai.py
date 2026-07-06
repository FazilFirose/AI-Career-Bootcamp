import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from utils.cache import get_cached_result, save_to_cache
import json

load_dotenv()  # reads the .env file

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_text(text):
    """
    Takes extracted PDF text and returns a condensed summary
    with only the key points.
    """
    prompt = f"""
    You are an expert study assistant. Read the following study material
    and produce a condensed summary containing ONLY the most important
    key points a student needs to know. Remove filler, examples, and
    repetition. Use short bullet points.

    Study material:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
def search_subject_info(subject_code):
    """
    Searches for KTU subject syllabus + past paper patterns for a given
    subject code. Uses cache to avoid repeating searches for the same subject.
    """
    cached = get_cached_result(subject_code)
    if cached:
        return cached  # already searched before, reuse it

    prompt = f"""
    CONFIRMED FACTS about KTU (APJ Abdul Kalam Technological University)
    2024 Scheme — treat these as ground truth, do not contradict them:
    - Total university exam marks per subject: 60 (NOT 100 — that was
      the old 2019 scheme)
    - Number of modules per subject: 4 (NOT 5 — that was the old 2019
      scheme)
    - Exam pattern: Part A = 24 marks, Part B = 36 marks
      (the old 2019 scheme was Part A = 30 marks, Part B = 70 marks —
      do NOT use these old numbers)
    - The official syllabus and model question papers are published
      by KTU directly at ktu.edu.in, under the Academic section
      (view-questionpapers) and per-semester pages like
      ktu.edu.in/academics/btech/question-papers/semester-X

    Search for information about the KTU subject with code {subject_code}.
    Prioritize ktu.edu.in as the source wherever possible. Find:
    1. The official 2024-scheme syllabus/module breakdown for this
       subject (must be exactly 4 modules)
    2. Any available 2024-scheme previous year or model question papers
       specifically (2019-scheme papers may only be used for comparing
       topic patterns, never for marks/pattern)
    3. Commonly repeated or emphasized topics across available papers
    4. Confirm the marking pattern matches: 60 total marks, 24 (Part A)
       + 36 (Part B). If a source states different numbers, disregard
       that source as outdated/incorrect.

    Summarize your findings clearly, organized by module. Do not
    present any 2019-scheme numbers as if they apply to 2024.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )

    result = response.text
    save_to_cache(subject_code, result)
    return result
def generate_study_map(combined_text, subject_code, subject_info, days_left):
    """
    Combines uploaded PDF content + web-researched subject info to produce
    a prioritized, exam-date-aware study map. Returns a dict with:
    - 'modules': list of {name, difficulty_score, summary} for charting
    - 'details': dict of {module_name: full detailed text with questions}
    """
    prompt = f"""
    You are an expert exam strategist helping a KTU student prepare for
    subject {subject_code}. The student has {days_left} days left.

    Student's uploaded material:
    ---
    {combined_text}
    ---

    Researched subject info (syllabus, past papers, marking scheme):
    ---
    {subject_info}
    ---

    Respond with ONLY a valid JSON object (no markdown, no extra text),
    in exactly this structure:

    {{
      "modules": [
        {{
          "name": "Module 1: <topic name>",
          "difficulty_score": <integer 1-10, where 1 = easiest/fastest
                               to master, 10 = hardest/most time-consuming>,
          "study_order": <integer, 1 = study first>,
          "key_points": ["point 1", "point 2", "..."],
          "likely_questions": [
            {{
              "question": "the likely exam question text",
              "marks": <integer mark value based on 2024 scheme Part A/B>,
              "model_answer": "the actual content/points the student
                               should write to answer this well",
              "needs_diagram": true or false,
              "diagram_search_term": "short search term if needs_diagram
                                       is true, else empty string"
            }}
          ]
        }}
      ]
    }}

    Include all 4 modules (fill gaps from research if the student's
    uploaded material doesn't cover a module). Order modules by
    study_order based on ease-of-mastery (easiest first), not just
    importance, considering the {days_left} days available.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    try:
        data = json.loads(response.text)
    except json.JSONDecodeError as e:
        print("RAW GEMINI OUTPUT (for debugging):")
        print(response.text)
        raise e

    return data
def detect_modules(file_snippets, subject_info):
    """
    Given short text snippets from each uploaded file, and the subject's
    known module breakdown, determine which module each file covers.
    file_snippets: dict like {"notes1.pdf": "first 500 words...", ...}
    """
    snippets_text = ""
    for filename, snippet in file_snippets.items():
        snippets_text += f"\n\nFile: {filename}\nContent snippet:\n{snippet}"

    prompt = f"""
    Here is the module breakdown for this subject (from research):
    {subject_info}

    Here are snippets from files a student uploaded:
    {snippets_text}

    For each file, identify which module (by number and short topic name)
    its content most closely matches. Respond in this exact format, one
    line per file:

    filename -> Module X: Topic Name

    If a file doesn't clearly match any module, write:
    filename -> Unclear / General notes
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text