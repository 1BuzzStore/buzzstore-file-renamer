import streamlit as st
import os
import io
import zipfile
import json
import random
import string
import smtplib
import sqlite3
import time
import threading
import re
import base64

# ✅ Page config
st.set_page_config(page_title="BuzzStore File Renamer", page_icon="📂", layout="centered")

# ✅ Load logo safely
def load_logo_b64(path="buzzstore_logo.png"):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""  # no logo fallback

logo_b64 = load_logo_b64()
logo_html = f'<img src="data:image/png;base64,{logo_b64}" width="120" alt="BuzzStore Logo">' if logo_b64 else ""

# ✅ Dark mode + glassy UI
st.markdown(
    f"""
    <style>
      /* Global dark theme */
      body {{
        background-color: #0e0e17;
        color: #f0f0f0;
      }}
      .stApp {{
        background-color: #0e0e17;
      }}

      /* ---- Glassy Header ---- */
      .glass-header {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        margin-bottom: 25px;
      }}
      .glass-header h1 {{
        color: #A540F5;
        font-size: 2em;
        margin: 15px 0 10px 0;
      }}
      .glass-header p {{
        color: #bbb;
        font-size: 1.05em;
        margin: 0;
      }}

      /* ---- Inputs (Text fields, file uploader, checkbox) ---- */
      .stTextInput > div > div > input,
      .stTextInput > div > div > textarea,
      .stFileUploader > div > div {{
          background: rgba(255, 255, 255, 0.07) !important;
          color: #000 !important;
          border-radius: 12px !important;
          border: 1px solid rgba(255,255,255,0.15) !important;
          padding: 10px 14px !important;
          font-size: 1em !important;
      }}
      .stTextInput > div > div > input:focus,
      .stTextInput > div > div > textarea:focus {{
          border: 1px solid #A540F5 !important;
          box-shadow: 0 0 8px #A540F5 !important;
          outline: none !important;
      }}

      /* ---- Checkbox ---- */
      .stCheckbox > label {{
          color: #A540F5 !important;
          font-weight: 500 !important;
      }}

      /* ---- Buttons ---- */
      .stButton > button {{
          background-color: #00BF63 !important;
          color: white !important;
          border-radius: 12px !important;
          padding: 10px 20px !important;
          border: none !important;
          font-weight: bold !important;
      }}
      .stButton > button:hover {{
          background-color: #A540F5 !important;
          box-shadow: 0px 0px 10px #A540F5;
      }}
    </style>

    <div class="glass-header">
      <a href="https://store.buzznest.space" target="_blank" rel="noopener">
        {logo_html}
      </a>
      <h1>BuzzStore File Renamer</h1>
      <p>Easily rename and organize your files in bulk. Upload → Rename → Download. 🚀</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ Upload files
uploaded_files = st.file_uploader("Upload your files", accept_multiple_files=True)

# ✅ User inputs
prefix = st.text_input("File Prefix", value="File")
add_numbering = st.checkbox("Add numbering", value=True)

# ✅ Rename & download
if uploaded_files and st.button("Rename Files"):
    with tempfile.TemporaryDirectory() as tmpdirname:
        count = 1
        renamed_files = []

        # Save + rename uploaded files
        for file in uploaded_files:
            ext = os.path.splitext(file.name)[1]
            if add_numbering:
                new_name = f"{prefix}_{count}{ext}"
            else:
                new_name = f"{prefix}{ext}"
            file_path = os.path.join(tmpdirname, new_name)
            with open(file_path, "wb") as f:
                f.write(file.read())
            renamed_files.append(file_path)
            count += 1

        # Zip renamed files
        zip_path = os.path.join(tmpdirname, "renamed_files.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in renamed_files:
                zipf.write(file, os.path.basename(file))

        # Download link
        with open(zip_path, "rb") as f:
            st.download_button("⬇️ Download Renamed Files", f, "renamed_files.zip")
