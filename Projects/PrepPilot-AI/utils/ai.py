import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from utils.cache import get_cached_result, save_to_cache

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
    IMPORTANT CONTEXT: KTU (APJ Abdul Kalam Technological University)
    introduced a NEW curriculum scheme in 2024. Under this new scheme:
    - Total exam marks per subject changed from 100 (old 2019 scheme)
      to 60 (new 2024 scheme)
    - Each subject now typically has 4 modules instead of 5
    - The Part A / Part B mark distribution is DIFFERENT from the old
      2019 scheme

    Search for information about the KTU subject with code {subject_code}.
    Find:
    1. The official 2024-scheme syllabus/module breakdown for this
       subject (should be 4 modules, NOT 5)
    2. Any available 2024-scheme previous year question papers
       specifically (do NOT use 2019-scheme papers for marking pattern,
       only for topic-pattern comparison)
    3. Commonly repeated or emphasized topics across available papers
    4. The EXACT 2024-scheme exam marking/evaluation pattern for this
       subject — total marks should be 60, confirm the Part A vs
       Part B mark distribution specifically for 2024, not 2019

    If you find conflicting information between 2019 and 2024 scheme
    sources, explicitly state which scheme each detail comes from, and
    prioritize 2024-scheme information for anything related to marks
    or exam pattern.

    Summarize your findings clearly, organized by module, and clearly
    label which scheme (2019 or 2024) each piece of information is
    based on.
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
    a prioritized, exam-date-aware study map with per-module likely
    questions, expected marks, and answer-length guidance.
    """
    prompt = f"""
    You are an expert exam strategist helping a KTU (APJ Abdul Kalam
    Technological University) student prepare for subject {subject_code}.

    The student has {days_left} days left before their exam.

    Here is the student's own uploaded study material (may only cover
    SOME of the subject's modules):
    ---
    {combined_text}
    ---

    Here is researched information about this subject's syllabus,
    module breakdown, past papers (2019 and 2024 scheme), and the
    2024 scheme's marking/evaluation pattern:
    ---
    {subject_info}
    ---

    Your task:
    1. Identify all modules for this subject (usually 4-5 in the 2024
       scheme). For any module NOT covered in the student's uploaded
       material, use the researched information to fill that gap.
    2. Rank ALL modules in priority order (most important/most-likely
       tested first), considering the {days_left} days available —
       if time is short, prioritize more aggressively.
    3.  For EACH module, provide:
       - Condensed key points only (no filler)
       - The most likely exam questions for that module
       - The likely mark value of each question (based on the 2024
         scheme's marking pattern, e.g., Part A short answers vs
         Part B long answers)
       - For each likely question, WRITE OUT the actual model answer
         content the student should study and reproduce — not just
         instructions on how much to write. Give the real points,
         explanations, or steps needed to answer that specific
         question well and score full marks for its mark value.

    Format the output as a clear, structured study map organized by
    priority, easy to scan quickly under time pressure.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
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