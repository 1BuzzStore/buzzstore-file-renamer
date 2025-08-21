import streamlit as st
import os
import io
import zipfile
import uuid
import hashlib
import json

# ---------------------------
# SESSION STATE SETUP
# ---------------------------
if "view" not in st.session_state:
    st.session_state.view = "free"
if "premium_logged_in" not in st.session_state:
    st.session_state.premium_logged_in = False
if "email" not in st.session_state:
    st.session_state.email = None

# ---------------------------
# USERS DATA STORAGE
# ---------------------------
USERS_FILE = "users.json"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

with open(USERS_FILE, "r") as f:
    users = json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------------------
# NAVIGATION
# ---------------------------
def show_free():
    st.title("🆓 Free File Renamer")
    st.info("📦 Free Plan: Upload up to **5 files**, max **50MB each**")
    max_files = 5
    max_size_mb = 50

    uploaded_files = st.file_uploader(
        f"Upload files to rename (Max {max_files} files, {max_size_mb}MB each)",
        accept_multiple_files=True,
        key="free_files"
    )
    prefix = st.text_input("Enter prefix for renamed files", value="buzzstore", key="free_prefix")

    if st.button("Rename Files (Free)"):
        if uploaded_files:
            if len(uploaded_files) > max_files:
                st.warning("⚠️ You’ve exceeded free plan limits! Apply for Premium to continue.")
                if st.button("➡️ Go to Premium"):
                    st.session_state.view = "premium_login"
                    st.experimental_rerun()
            else:
                oversized = [f.name for f in uploaded_files if (len(f.getbuffer()) / (1024*1024)) > max_size_mb]
                if oversized:
                    st.warning(f"⚠️ The following files exceed {max_size_mb}MB: {', '.join(oversized)}")
                else:
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                        for i, f in enumerate(uploaded_files, start=1):
                            ext = os.path.splitext(f.name)[1]
                            new_name = f"{prefix}_{i}{ext}"
                            zip_file.writestr(new_name, f.getbuffer())
                    zip_buffer.seek(0)
                    st.success("✅ Files renamed successfully!")
                    st.download_button("⬇️ Download Renamed Files (ZIP)", zip_buffer, "renamed_files.zip", "application/zip")
        else:
            st.warning("⚠️ Please upload at least one file.")

# ---------------------------
# PREMIUM LOGIN / REGISTER
# ---------------------------
def show_premium_login():
    st.title("💎 Premium Login / Register")
    tab = st.radio("Choose option", ["Login", "Register", "Forgot Password"])
    email = st.text_input("Email", key="email")
    password = st.text_input("Password", type="password", key="password")

    if tab == "Register":
        if st.button("Register"):
            if not email or not password:
                st.error("Email and password required!")
            elif email in users:
                st.error("Email already registered!")
            else:
                token = str(uuid.uuid4())
                users[email] = {"password": hash_password(password), "token": token}
                save_users(users)
                st.success(f"Registered! Your access token: {token}")
                st.session_state.email = email
                if st.button("➡️ Go to Premium Access Token"):
                    st.session_state.view = "premium_token"
                    st.experimental_rerun()

    elif tab == "Login":
        if st.button("Login"):
            user = users.get(email)
            if not user:
                st.error("Email not found!")
            elif user["password"] != hash_password(password):
                st.error("Incorrect password!")
            else:
                st.success("✅ Login successful!")
                st.session_state.email = email
                if st.button("➡️ Enter Premium Token"):
                    st.session_state.view = "premium_token"
                    st.experimental_rerun()

    elif tab == "Forgot Password":
        if st.button("Reset Password"):
            user = users.get(email)
            if not user:
                st.error("Email not found!")
            else:
                new_password = str(uuid.uuid4())[:8]
                users[email]["password"] = hash_password(new_password)
                save_users(users)
                st.success(f"✅ Password reset! New password: {new_password}")

    if st.button("⬅️ Back to Free"):
        st.session_state.view = "free"
        st.experimental_rerun()

# ---------------------------
# PREMIUM TOKEN ENTRY
# ---------------------------
def show_premium_token():
    st.title("🔑 Enter Premium Access Token")
    token_input = st.text_input("Access Token", key="token_input")
    if st.button("Verify Token"):
        user = users.get(st.session_state.email)
        if user and token_input == user["token"]:
            st.session_state.premium_logged_in = True
            st.session_state.view = "premium"
            st.success("✅ Token verified! Premium access granted.")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid token!")

    if st.button("⬅️ Back to Free"):
        st.session_state.view = "free"
        st.experimental_rerun()

# ---------------------------
# PREMIUM FILE RENAMER
# ---------------------------
def show_premium():
    st.title("💎 Premium File Renamer")
    st.success("💎 Premium Plan: Unlimited files, max **200MB each**")
    max_size_mb = 200

    uploaded_files = st.file_uploader(
        f"Upload files to rename (Max {max_size_mb}MB each)",
        accept_multiple_files=True,
        key="premium_files"
    )
    prefix = st.text_input("Enter prefix for renamed files", value="buzzstore", key="premium_prefix")

    if st.button("Rename Files (Premium)"):
        if uploaded_files:
            oversized = [f.name for f in uploaded_files if (len(f.getbuffer()) / (1024*1024)) > max_size_mb]
            if oversized:
                st.error(f"❌ The following files exceed {max_size_mb}MB: {', '.join(oversized)}")
            else:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for i, f in enumerate(uploaded_files, start=1):
                        ext = os.path.splitext(f.name)[1]
                        new_name = f"{prefix}_{i}{ext}"
                        zip_file.writestr(new_name, f.getbuffer())
                zip_buffer.seek(0)
                st.success("✅ Files renamed successfully!")
                st.download_button("⬇️ Download Renamed Files (ZIP)", zip_buffer, "renamed_files.zip", "application/zip")
        else:
            st.warning("⚠️ Please upload at least one file.")

    if st.button("⬅️ Back to Free"):
        st.session_state.view = "free"
        st.experimental_rerun()

# ---------------------------
# MAIN NAVIGATION
# ---------------------------
if st.session_state.view == "free":
    show_free()
elif st.session_state.view == "premium_login":
    show_premium_login()
elif st.session_state.view == "premium_token":
    show_premium_token()
elif st.session_state.view == "premium":
    show_premium()