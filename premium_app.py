import streamlit as st
import os
import io
import zipfile

st.set_page_config(page_title="Buzzstore Premium File Renamer")

st.title("💎 Premium File Renamer")
st.success("💎 Premium Plan: Unlimited files, max **200MB each**")

max_size_mb = 200

uploaded_files = st.file_uploader(
    f"Upload files to rename (Max {max_size_mb}MB each)",
    accept_multiple_files=True
)

prefix = st.text_input("Enter prefix for renamed files", value="buzzstore")

if st.button("Rename Files"):
    if uploaded_files:
        # Validate file sizes
        oversized_files = [
            f.name for f in uploaded_files if (len(f.getbuffer()) / (1024 * 1024)) > max_size_mb
        ]
        if oversized_files:
            st.error(
                f"❌ The following files exceed the {max_size_mb}MB limit: {', '.join(oversized_files)}"
            )
        else:
            # Create in-memory ZIP
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for i, uploaded_file in enumerate(uploaded_files, start=1):
                    ext = os.path.splitext(uploaded_file.name)[1]
                    new_name = f"{prefix}_{i}{ext}"
                    zip_file.writestr(new_name, uploaded_file.getbuffer())
            zip_buffer.seek(0)
            st.success("✅ Files renamed successfully!")
            st.download_button(
                label="⬇️ Download Renamed Files (ZIP)",
                data=zip_buffer,
                file_name="renamed_files.zip",
                mime="application/zip"
            )
    else:
        st.warning("⚠️ Please upload at least one file.")