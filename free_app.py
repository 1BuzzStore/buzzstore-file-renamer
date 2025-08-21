import streamlit as st
import os
import io
import zipfile

# ---------------------------
# Free File Renamer
# ---------------------------
st.title("🆓 Free File Renamer")

# Free plan limits
MAX_FILES = 5
MAX_SIZE_MB = 50
st.info(f"📦 Free Plan: Upload up to **{MAX_FILES} files**, max **{MAX_SIZE_MB}MB each**")

uploaded_files = st.file_uploader(
    f"Upload files (Max {MAX_FILES} files, {MAX_SIZE_MB}MB each)",
    accept_multiple_files=True
)
prefix = st.text_input("Enter prefix for renamed files", value="buzzstore")

if st.button("Rename Files"):
    if not uploaded_files:
        st.warning("⚠️ Please upload at least one file.")
    elif len(uploaded_files) > MAX_FILES:
        st.error(f"❌ Free users can only upload up to {MAX_FILES} files.")
    else:
        oversized = [f.name for f in uploaded_files if len(f.getbuffer()) / (1024 * 1024) > MAX_SIZE_MB]
        if oversized:
            st.error(f"❌ These files exceed {MAX_SIZE_MB}MB: {', '.join(oversized)}")
        else:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for i, f in enumerate(uploaded_files, start=1):
                    ext = os.path.splitext(f.name)[1]
                    zip_file.writestr(f"{prefix}_{i}{ext}", f.getbuffer())
            zip_buffer.seek(0)
            st.success("✅ Files renamed successfully!")
            st.download_button("⬇️ Download Renamed Files (ZIP)", zip_buffer, "renamed_files.zip", "application/zip")