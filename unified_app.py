import streamlit as st
import os
import io
import zipfile

# ---------------------------
# PLAN CONFIG
# ---------------------------
FREE_MAX_FILES = 5
FREE_MAX_MB = 50

PREMIUM_MAX_FILES = None  # Unlimited
PREMIUM_MAX_MB = 200

# ---------------------------
# SESSION STATE
# ---------------------------
if "plan" not in st.session_state:
    st.session_state.plan = "free"  # default to free
if "view" not in st.session_state:
    st.session_state.view = "free"  # what is currently shown

# ---------------------------
# FUNCTIONS
# ---------------------------
def rename_files(uploaded_files, prefix, max_mb):
    """Renames files and returns in-memory zip"""
    oversized_files = [
        f.name for f in uploaded_files if (len(f.getbuffer()) / (1024 * 1024)) > max_mb
    ]
    if oversized_files:
        st.error(
            f"❌ The following files exceed the {max_mb}MB limit: {', '.join(oversized_files)}"
        )
        return

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

# ---------------------------
# LAUNCHER
# ---------------------------
st.title("📝 Buzzstore File Renamer Launcher")

# Plan switcher
col1, col2 = st.columns(2)
with col1:
    if st.button("Use Free Plan"):
        st.session_state.plan = "free"
        st.session_state.view = "free"
with col2:
    if st.button("Use Premium Plan"):
        st.session_state.plan = "premium"
        st.session_state.view = "premium"

# ---------------------------
# FREE PLAN VIEW
# ---------------------------
if st.session_state.view == "free":
    st.subheader("🆓 Free File Renamer")
    st.info(f"Upload up to {FREE_MAX_FILES} files, max {FREE_MAX_MB}MB each")

    uploaded_files = st.file_uploader(
        f"Upload files (Max {FREE_MAX_FILES} files, {FREE_MAX_MB}MB each)",
        accept_multiple_files=True
    )
    prefix = st.text_input("Enter prefix for renamed files", value="buzzstore_free")

    if st.button("Rename Files (Free)"):
        if uploaded_files:
            if len(uploaded_files) > FREE_MAX_FILES:
                st.error(f"❌ Free users can upload up to {FREE_MAX_FILES} files only.")
            else:
                rename_files(uploaded_files, prefix, FREE_MAX_MB)
        else:
            st.warning("⚠️ Please upload at least one file.")

# ---------------------------
# PREMIUM PLAN VIEW
# ---------------------------
if st.session_state.view == "premium":
    st.subheader("💎 Premium File Renamer")
    st.success(f"Unlimited files, max {PREMIUM_MAX_MB}MB each")

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