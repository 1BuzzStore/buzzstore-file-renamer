import streamlit as st
import os
import io
import zipfile

FREE_MAX_FILES = 5
FREE_MAX_MB = 50

st.title("🆓 Free File Renamer")
st.info(f"📦 Free Plan: Upload up to **{FREE_MAX_FILES} files**, max **{FREE_MAX_MB}MB each**")

uploaded_files = st.file_uploader(
    f"Upload files to rename (Max {FREE_MAX_FILES} files, {FREE_MAX_MB}MB each)",
    accept_multiple_files=True
)
prefix = st.text_input("Enter prefix for renamed files", value="buzzstore")

if st.button("Rename Files"):
    if uploaded_files:
        if len(uploaded_files) > FREE_MAX_FILES:
            st.error(f"❌ Free users can only upload up to {FREE_MAX_FILES} files.")
        else:
            oversized = [f.name for f in uploaded_files if (len(f.getbuffer()) / (1024*1024)) > FREE_MAX_MB]
            if oversized:
                st.error(f"❌ Files exceed {FREE_MAX_MB}MB: {', '.join(oversized)}")
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

if st.button("Switch to Premium"):
    st.session_state.plan = "premium"
    st.experimental_rerun()