import streamlit as st
import os, zipfile, io

# Premium plan: 200MB
st.set_option("server.maxUploadSize", 200)

# ---------------------------
# Dummy User Database
# ---------------------------
USERS = {
    "premium_user": {"password": "456", "plan": "premium"},
}

st.set_page_config(page_title="Buzzstore Premium Tool", page_icon="💎", layout="centered")
st.title("💎 Buzzstore Tools - Premium Edition")

# ---------------------------
# Login
# ---------------------------
if "user" not in st.session_state:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state["user"] = USERS[username]
            st.rerun()
        else:
            st.error("❌ Invalid login")
else:
    plan = st.session_state["user"]["plan"]

    st.sidebar.title("User Panel")
    st.sidebar.write("👤 Premium Plan")
    if st.sidebar.button("Logout"):
        del st.session_state["user"]
        st.rerun()

    # ---------------------------
    # File Renamer
    # ---------------------------
    st.subheader("⚡ File Renamer (Premium Plan)")
    st.success("💎 Premium Plan: Unlimited files, max **200MB each**")

    uploaded_files = st.file_uploader(
        "Upload files (max 200MB each)",
        accept_multiple_files=True
    )
    prefix = st.text_input("Prefix", "buzzstore")

    if st.button("Rename Files"):
        if uploaded_files:
            oversized_files = [
                f.name for f in uploaded_files if (len(f.getbuffer()) / (1024 * 1024)) > 200
            ]
            if oversized_files:
                st.error(f"❌ Files exceed 200MB: {', '.join(oversized_files)}")
            else:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for i, f in enumerate(uploaded_files, 1):
                        ext = os.path.splitext(f.name)[1]
                        zip_file.writestr(f"{prefix}_{i}{ext}", f.getbuffer())
                zip_buffer.seek(0)
                st.download_button("⬇️ Download", zip_buffer, "renamed_files.zip", "application/zip")
        else:
            st.warning("⚠️ Upload at least one file.")