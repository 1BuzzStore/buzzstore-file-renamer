import streamlit as st
import os
import io
import zipfile
import uuid
import hashlib

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
    st.session_state.view = "free"  # free, premium_login, premium
if "premium_logged_in" not in st.session_state:
    st.session_state.premium_logged_in = False
if "users" not in st.session_state:
    st.session_state.users = {}  # email -> hashed password & token

# ---------------------------
# Helper Functions
# ---------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def rename_files(files, prefix, max_size_mb):
    oversized_files = [
        f.name for f in files if (len(f.getbuffer()) / (1024 * 1024)) > max_size_mb
    ]
    if oversized_files:
        st.error(f"❌ The following files exceed {max_size_mb}MB: {', '.join(oversized_files)}")
        return False

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
    return True

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

    exceeded = False
    if uploaded_files:
        if len(uploaded_files) > FREE_MAX_FILES or any(
            (len(f.getbuffer()) / (1024 * 1024)) > FREE_MAX_MB for f in uploaded_files
        ):
            exceeded = True

    if st.button("Rename Files (Free)"):
        if uploaded_files:
            if exceeded:
                st.warning("⚠️ You've exceeded Free plan limits!")
            else:
                rename_files(uploaded_files, prefix, FREE_MAX_MB)
        else:
            st.warning("⚠️ Please upload at least one file.")

    if exceeded:
        st.warning("⚠️ You've exceeded Free plan limits!")
        if st.button("Apply for Premium 💎"):
            st.session_state.view = "premium_login"
            st.stop()

# ---------------------------
# PREMIUM LOGIN / REGISTER VIEW
# ---------------------------
elif st.session_state.view == "premium_login":
    st.title("💎 Premium Login / Register")

    tab = st.radio("Choose option", ["Login", "Register"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if tab == "Register":
        if st.button("Register"):
            if email in st.session_state.users:
                st.error("Email already registered!")
            elif not email or not password:
                st.error("Email and password required!")
            else:
                token = str(uuid.uuid4())
                st.session_state.users[email] = {"password": hash_password(password), "token": token}
                st.success(f"Registered! Your access token: {token}")
                st.session_state.premium_logged_in = True
                st.session_state.view = "premium"
                st.stop()

    else:  # Login
        if st.button("Login"):
            user = st.session_state.users.get(email)
            if not user:
                st.error("Email not found!")
            elif user["password"] != hash_password(password):
                st.error("Incorrect password!")
            else:
                st.success("✅ Logged in successfully!")
                st.session_state.premium_logged_in = True
                st.session_state.view = "premium"
                st.stop()

    if st.button("⬅️ Back to Free"):
        st.session_state.view = "free"
        st.stop()

# ---------------------------
# PREMIUM FILE RENAMER VIEW
# ---------------------------
elif st.session_state.view == "premium":
    if not st.session_state.premium_logged_in:
        st.warning("You must login/register to access Premium features.")
        if st.button("Go to Login"):
            st.session_state.view = "premium_login"
            st.stop()
    else:
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

        if st.button("⬅️ Back to Free"):
            st.session_state.view = "free"
            st.stop()