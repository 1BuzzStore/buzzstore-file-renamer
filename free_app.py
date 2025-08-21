import streamlit as st
import os
import io
import zipfile

# ---------------------------
# File Renamer (Free Feature)
# ---------------------------
st.title("🆓 Free File Renamer")

# Show plan limits clearly
st.info("📦 Free Plan: Upload up to **5 files**, max **50MB each**")

max_files = 5
max_size_mb = 50

uploaded_files = st.file_uploader(
    f"Upload files to rename (Max {max_files} files, {max_size_mb}MB each)",
    accept_multiple_files=True
)
prefix = st.text_input("Enter prefix for renamed files", value="buzzstore")

if st.button("Rename Files"):
    if uploaded_files:
        # Check number of files
        if len(uploaded_files) > max_files:
            st.error(f"❌ Free users can only upload up to {max_files} files.")
        else:
            # Validate file sizes
            oversized_files = [
                f.name for f in uploaded_files if (len(f.getbuffer()) / (1024 * 1024)) > max_size_mb
            ]
            if oversized_files:
                st.error(
                    f"❌ The following files exceed the {max_size_mb}MB limit: {', '.join(oversized_files)}"
                )
            else:
                # Create an in-memory zip file
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for i, uploaded_file in enumerate(uploaded_files, start=1):
                        file_extension = os.path.splitext(uploaded_file.name)[1]
                        new_name = f"{prefix}_{i}{file_extension}"
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