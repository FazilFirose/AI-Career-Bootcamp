import streamlit as st
import os
from PyPDF2 import PdfReader
import math
import re
from datetime import datetime, date
import io
from utils.ai import summarize_text, search_subject_info, generate_study_map, detect_modules

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
st.set_page_config(
    page_title="PrepPilot AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 PrepPilot AI")
st.subheader("Your AI-Powered Study Assistant")

st.markdown("---")

st.write("""
Welcome to **PrepPilot AI**!

Upload your study materials and let AI help you build a winning exam strategy.
""")

st.markdown("### Step 1: Upload your study materials")
uploaded_files = st.file_uploader(
    "📄 Upload one or more PDFs (any modules you have notes for)",
    type=["pdf"],
    accept_multiple_files=True
)

st.markdown("### Step 2: Subject details")
subject_code = st.text_input(
    "📘 KTU Subject Code",
    placeholder="Example: CST301"
).strip().upper()

exam_date = st.date_input("📅 Exam Date")

generate_clicked = st.button("🎯 Generate Study Map")


@st.cache_data
def extract_pdf_text(file_bytes, file_name):
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text, len(reader.pages)


if generate_clicked:
    if not uploaded_files:
        st.error("Please upload at least one PDF before generating a study map.")
    elif not subject_code:
        st.error("Please enter your KTU subject code.")
    else:
        combined_text = ""
        file_snippets = {}

        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.getvalue()
            text, page_count = extract_pdf_text(file_bytes, uploaded_file.name)
            combined_text += f"\n\n--- Content from {uploaded_file.name} ---\n{text}"
            file_snippets[uploaded_file.name] = text[:800]  # short snippet for module detection

        with st.spinner(f"Step 1/3: Researching {subject_code} syllabus..."):
            subject_info = search_subject_info(subject_code)

        with st.spinner("Step 2/3: Matching your files to modules..."):
            module_mapping = detect_modules(file_snippets, subject_info)

        st.markdown("### 📊 Your Files, Mapped to Modules")
        st.markdown(module_mapping)

        days_left = (exam_date - date.today()).days
        if days_left < 0:
            st.warning("The exam date you entered is in the past. Please check the date.")
        else:
            st.info(f"⏳ {days_left} day(s) left until your exam.")
        with st.spinner("Step 3/3: Building your personalized study map..."):
            study_map = generate_study_map(
                combined_text=combined_text,
                subject_code=subject_code,
                subject_info=subject_info,
                days_left=days_left
            )

        st.markdown("---")
        st.markdown("## 🗺️ Your Study Map")
        st.markdown(study_map)


st.sidebar.title("PrepPilot AI")
st.sidebar.success("Version 2.0")