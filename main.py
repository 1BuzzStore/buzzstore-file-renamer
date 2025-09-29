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
st.set_page_config(page_title="Buzz File Renamer", page_icon="📂", layout="centered")

with open("buzzstore_logo.png", "rb") as f:
    logo_bytes = f.read()
logo_b64 = base64.b64encode(logo_bytes).decode()
# ✅ Floating top logo
header_logo_html = f"""
<style>
.header-logo {{
    position: fixed;
    top: 20px;  /* distance from top */
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    z-index: 9999;  /* stay on top */
}}
.header-logo img {{
    width: 120px;  /* adjust size */
    opacity: 0.95;
}}
</style>
<div class="header-logo">
    <img src="data:image/png;base64,{logo_b64}" alt="BuzzStore Logo">
</div>
"""
st.markdown(header_logo_html, unsafe_allow_html=True)



#hide limit 200mb per section
hide_file_uploader_style = """
<style>
.st-emotion-cache-14503gc {
    font-size: 0.875rem;
    color: rgba(49, 51, 63, 0.6);
    display: none;
}
</style>
"""
st.markdown(hide_file_uploader_style, unsafe_allow_html=True)

# ===================== THEME / STYLES =====================
# Custom Styling
st.markdown("""

<style>

/* PAGE BACKGROUND */
.stApp {
  background:
    radial-gradient(80% 120% at 0% 0%, rgba(165,64,245,0.18), transparent 60%),
    radial-gradient(70% 100% at 100% 0%, rgba(0,191,99,0.12), transparent 60%),
    linear-gradient(180deg, #0f0f14 0%, #0a0a0e 100%);
  padding-top: 2rem !important;
  margin-top: 0 !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
  background: rgba(20,20,20,0.72) !important;
  backdrop-filter: blur(12px);
  border-right: 1px solid rgba(255,255,255,0.08);

}

/* BUTTONS */
.stButton > button,
[data-testid="baseButton-secondary"] {
  background-color: #00BF63 !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  transition: all 0.2s ease-in-out;
}
.stButton > button:hover,
[data-testid="baseButton-secondary"]:hover {
  background-color: #A540F5 !important;
  color: #fff !important;
  transform: scale(1.05);
}

/* WIDGET LABELS */
label[data-testid="stWidgetLabel"] > div > p {
  color: #fff !important;
}

/* ALERT / INFO BLOCKS */
div[role="alert"] {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(165,64,245,0.35) !important;
}
div[role="alert"] * {
  color: #fff !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploaderDropzone"] {
  background: rgba(255,255,255,0.06) !important;
  border: 1px dashed rgba(255,255,255,0.25) !important;
  border-radius: 12px !important;
}
[data-testid="stFileUploaderDropzone"] * {
  color: #fff !important;
}
[data-testid="stFileUploaderDropzone"] > div > div {
  background: transparent !important;
}

/* FILE INPUT FIELD */
input[type="file"] {
  background: transparent !important;
  color: #fff !important;
  border: 1px solid rgba(255,255,255,0.15) !important;
  border-radius: 10px !important;
}

/* TEXT INPUTS & TEXTAREAS */
.stTextInput input,
.stTextArea textarea {
  color: #A540F5 !important;
  background-color: #F4FAFF !important;
  border: 1px dashed rgba(255,255,255,0.25) !important;
  border-radius: 10px !important;
}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
  color: #A540F5 !important;
  opacity: 1 !important;
}

/* GENERAL INPUT STYLE */
input, textarea {
  background-color: transparent !important;
  color: #fff !important;
  border-radius: 10px !important;
  border: 1px solid rgba(255,255,255,0.15) !important;

}

/* RADIO BUTTON TEXT */
div[role="radiogroup"] label p {
  color: #fff !important;
}

/* MARKDOWN TEXT */
div[data-testid="stMarkdownContainer"] li,
div[data-testid="stMarkdownContainer"] p {
  color: #fff !important;
}

/* GLOBAL ACCENT COLOR */
:root, .stApp {
  --brand-color: #A540F5;
}

/* TITLES */
h1, h2, h3 {
  color: #A540F5 !important;
}

/* MAIN CONTENT WRAPPER */
.block-container {
  background: rgba(15,15,20,0.55);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 2rem 2.2rem;
  margin-top: 3rem !important;
  margin-bottom: 2rem !important;
}

.st-emotion-cache-pd6qx2 {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    color: #00BF63;
    font-size: 1.5rem;
    width: 1.5rem;
    height: 1.5rem;
    user-select: none;
    /* font-family removed to avoid Material Icons issue */
    font-weight: 400;
    font-style: normal;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    white-space: nowrap;
    overflow-wrap: normal;
    direction: ltr;
    -webkit-font-smoothing: antialiased;
}

.st-emotion-cache-jzs692 {
    display: inline-flex;
    background-color: rgb(45 45 45);
    border: 1px solid rgba(151, 166, 195, 0.15);
}

.st-emotion-cache-1ffuo7c {
    background: rgb(45 45 45);
}

.st-emotion-cache-1pbsqtx {
    fill: rgb(255 255 255);
}

.st-emotion-cache-egm30d {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    border-radius: 0.5rem;
    margin: 0px 0.125rem;
    text-transform: none;
    font-family: inherit;
    color: rgb(255 255 255);
    width: auto;
    cursor: pointer;
    user-select: none;
    background-color: transparent;
    border: none;
    padding: 0px 0.5rem;
    font-size: 0.875rem;
    line-height: 1;
    min-width: 1.75rem;
    min-height: 1.75rem;
}

.st-emotion-cache-5qfegl {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 2.5rem;
    margin: 0px;
    line-height: 1.6;
    text-transform: none;
    font-size: inherit;
    font-family: inherit;
    color: inherit;
    width: 100%;
    cursor: pointer;
    user-select: none;
    background-color: rgb(45 45 45);
    border: 1px solid rgba(49, 51, 63, 0.2);
}

</style>
""", unsafe_allow_html=True)

# ---------- CONFIG ----------
FREE_MAX_FILES = 5
FREE_MAX_MB = 50
PREMIUM_MAX_MB = 200

# ===================== MAIN UI =====================

# ---------- FREE SECTION ----------
if not st.session_state.premium_active:
    st.subheader("Free Plan")
    st.info(f"Upload up to **{FREE_MAX_FILES} files**, max **{FREE_MAX_MB}MB each**")

    free_uploaded = st.file_uploader("Upload files (Free Plan)", accept_multiple_files=True, key="free_uploader")   
    prefix_free = st.text_input("Enter prefix for renamed files (Free)", value="buzzstore", key="prefix_free")      

    if st.button("Rename Files (Free)", use_container_width=True):
        if not free_uploaded:
            st.warning("Please upload at least one file.")
        elif len(free_uploaded) > FREE_MAX_FILES:
            st.warning("You exceeded free plan limits. Upgrade to Premium.")
        else:
            oversized = [f.name for f in free_uploaded if (len(f.getbuffer()) / (1024 * 1024)) > FREE_MAX_MB]       
            if oversized:
                st.error(f"These files exceed {FREE_MAX_MB}MB: {', '.join(oversized)}")
            else:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for i, uploaded_file in enumerate(free_uploaded, start=1):
                        ext = os.path.splitext(uploaded_file.name)[1]
                        new_name = f"{prefix_free}_{i}{ext}"
                        zip_file.writestr(new_name, uploaded_file.getbuffer())
                zip_buffer.seek(0)
                flash_success("Files renamed successfully.")  # 10s flash
                st.download_button("Download Renamed Files (ZIP)", zip_buffer, "renamed_files.zip", "application/zip")

    st.info("""
    Coming Soon
    - Auto-clean Excel files
    - Email report generator  
    (Currently available: Bulk rename files)
    """)



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
