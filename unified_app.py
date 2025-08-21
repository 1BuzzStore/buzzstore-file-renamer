import streamlit as st
import os
import io
import zipfile

# ---------------------------
# Constants
# ---------------------------
FREE_MAX_FILES = 5
FREE_MAX_MB = 50
PREMIUM_MAX_MB = 200

# ---------------------------
# Session State Defaults
# ---------------------------
if "view" not in st.session_state:
    st.session_state.view = "free"  # free or premium
if "exceeded_limits" not in st.session_state:
    st.session_state.exceeded_limits = False

# ---------------------------
# Helper Function
# ---------------------------
def rename_files(files, prefix, max_size_mb):
    oversized_files = [
        f.name for f in files if (len(f.getbuffer()) / (1024 * 1024)) > max_size_mb
    ]
    if oversized_files:
        st.error(f"❌ The following files exceed {max_size_mb}MB: {', '.join(oversized_files)}")
        return

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for i, uploaded_file in enumerate(files, start=1):
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

# ---------------------------
# FREE VIEW
# ---------------------------
if st.session_state.view == "free":
    st.title("🆓 Free File Renamer")
    st.info(f"Upload up to {FREE_MAX_FILES} files, max {FREE_MAX_MB}MB each")

    uploaded_files = st.file_uploader(
        f"Upload files (Max {FREE_MAX_FILES} files, {FREE_MAX_MB}MB each)",
        accept_multiple_files=True
    )
    prefix = st.text_input("Enter prefix for renamed files", value="buzzstore_free")

    if st.button("Rename Files (Free)"):
        if uploaded_files:
            if len(uploaded_files) > FREE_MAX_FILES or any(
                (len(f.getbuffer()) / (1024 * 1024)) > FREE_MAX_MB for f in uploaded_files
            ):
                st.session_state.exceeded_limits = True
                st.stop()  # immediately re-render
            else:
                rename_files(uploaded_files, prefix, FREE_MAX_MB)
        else:
            st.warning("⚠️ Please upload at least one file.")

    # Show Premium button only if limits exceeded
    if st.session_state.exceeded_limits:
        st.warning("⚠️ You've exceeded Free plan limits!")
        if st.button("Apply for Premium 💎"):
            st.session_state.view = "premium"
            st.session_state.exceeded_limits = False
            st.stop()  # immediately switch view

# ---------------------------
# PREMIUM VIEW
# ---------------------------
elif st.session_state.view == "premium":
    st.title("💎 Premium File Renamer")
    st.success(f"Upload unlimited files, max {PREMIUM_MAX_MB}MB each")

    uploaded_files = st.file_uploader(
        f"Upload files (Max {PREMIUM_MAX_MB}MB each)",
        accept_multiple_files=True
    )
    prefix = st.text_input("Enter prefix for renamed files", value="buzzstore_premium")

    if st.button("Rename Files (Premium)"):
        if uploaded_files:
            rename_files(uploaded_files, prefix, PREMIUM_MAX_MB)
        else:
            st.warning("⚠️ Please upload at least one file.")

    # Back to Free button
    if st.button("⬅️ Back to Free"):
        st.session_state.view = "free"
        st.stop()  # immediately switch back