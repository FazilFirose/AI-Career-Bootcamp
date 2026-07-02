import streamlit as st
import os
from PyPDF2 import PdfReader
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

Upload your study materials and let AI help you learn faster.
""")

uploaded_file = st.file_uploader(
    "📄 Upload a PDF",
    type=["pdf"]
)

if uploaded_file is not None:
     upload_path = os.path.join("uploads", uploaded_file.name)

     with open(upload_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

     st.success(f"✅ Uploaded: {uploaded_file.name}")
     st.write("📁 File saved successfully!")
     reader = PdfReader(upload_path)

     text = ""

     for page in reader.pages:
       text += page.extract_text() + "\n"

     st.subheader("📖 Extracted Text")

     st.text_area(
       "PDF Content",
        text,
        height=600
      )

st.sidebar.title("PrepPilot AI")
st.sidebar.success("Version 1")