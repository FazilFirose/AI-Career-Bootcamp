import streamlit as st
import os
from PyPDF2 import PdfReader
import math
import re
from datetime import datetime
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
     st.info(f"📄 Current File: {uploaded_file.name}")
     st.write("📁 File saved successfully!")
     reader = PdfReader(upload_path)

     text = ""

     for page in reader.pages:
       page_text = page.extract_text()

       if page_text:
          text += page_text + "\n"

     word_count = len(text.split())
     char_count = len(text)
     page_count = len(reader.pages)

     reading_time = math.ceil(word_count / 250)

     upload_time = datetime.now().strftime("%d %b %Y | %I:%M %p")
     st.markdown(
      """
       <h3 style="text-align:left;">📊 PDF Insights</h3>
     """,
     unsafe_allow_html=True
     )

     col1, col2 = st.columns(2)

     with col1:
      st.metric("📚 Pages", page_count)
      st.metric("📝 Words", word_count)

     with col2:
      st.metric("🔤 Characters", char_count)
      st.metric("⏱ Reading Time", f"{reading_time} min")

     st.caption(f"📅 Uploaded: {upload_time}")
     st.markdown("---")

     st.markdown("### 🔍 Search Inside PDF")

     search_query = st.text_input(
      "Search for a keyword or phrase",
       placeholder="Example: Machine Learning"
     )
     
     st.markdown("---")
     st.markdown("### 📖 PDF Content")

     display_text = text

     if search_query:
       pattern = re.compile(re.escape(search_query), re.IGNORECASE)

       display_text = pattern.sub(
        lambda m: (
         f'<span style="background:#00E5FF;'
         f'color:black;'
         f'padding:2px 4px;'
         f'border-radius:4px;'
         f'font-weight:bold;">{m.group()}</span>'
         ),
        text
       )

     st.markdown(
       f"""
      <div style="
        height:600px;
        overflow-y:auto;
        background:#1a1a1a;
        padding:20px;
        border-radius:12px;
        color:white;
        white-space:pre-wrap;
        border:1px solid #00E5FF;
      ">
     {display_text}
      </div>
      """,
      unsafe_allow_html=True
     )


     
st.sidebar.title("PrepPilot AI")
st.sidebar.success("Version 1.2")