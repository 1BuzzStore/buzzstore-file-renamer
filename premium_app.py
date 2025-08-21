import streamlit as st
import os
import io
import zipfile

PREMIUM_MAX_MB = 200

st.title("💎 Premium File Renamer")
st.success(f"💎 Premium Plan: Unlimited files, max **{PREMIUM_MAX_MB}MB each**")

uploaded_files = st.file_uploader(
    f"Upload files to rename (Max {PREMIUM_MAX_MB}MB each)",
    accept_multiple_files=True
)
prefix = st.text_input("Enter prefix for renamed files", value="buzzstore")

if st.button("Rename Files"):
    if uploaded_files:
        oversized = [f.name for f in uploaded_files if (len(f.getbuffer()) / (1024*1024)) > PREMIUM_MAX_MB]
        if oversized:
            st.error(f"❌ Files exceed {PREMIUM_MAX_MB}MB: {', '.join(oversized)}")
        else:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for i, f in enumerate(uploaded_files, start=1):
                    ext = os.path.splitext(f.name)[1]
                    zip_file.writestr(f"{prefix}_{i}{ext}", f.getbuffer())
            zip_buffer.seek(0)
            st.success("✅ Files renamed successfully!")
            st.download_button(
                label="⬇️ Download Renamed Files (ZIP)",
                data=zip_buffer,
                file_name="renamed_files.zip",
                mime="application/zip"
            )

if st.button("Switch to Free"):
    st.session_state.plan = "free"
    st.experimental_rerun()