import streamlit as st
import os, zipfile, io

# Free plan: 50MB
st.set_option("server.maxUploadSize", 50)

# ---------------------------
# Dummy User Database
# ---------------------------
USERS = {
    "free_user": {"password": "123", "plan": "free"},
}

st.set_page_config(page_title="Buzzstore Free Tool", page_icon="⚡", layout="centered")
st.title("⚡ Buzzstore Tools - Free Edition")

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
    st.sidebar.write("👤 Free Plan")
    if st.sidebar.button("Logout"):
        del st.session_state["user"]
        st.rerun()

    # ---------------------------
    # File Renamer
    # ---------------------------
    st.subheader("🆓 File Renamer (Free Plan)")
    st.info("📦 Free Plan: Upload up to **5 files**, max **50MB each**")

    uploaded_files = st.file_uploader(
        "Upload files (max 50MB each)",
        accept_multiple_files=True
    )
    prefix = st.text_input("Prefix", "buzzstore")

    if st.button("Rename Files"):
        if uploaded_files:
            if len(uploaded_files) > 5:
                st.error("❌ Free users can only upload up to 5 files.")
            else:
                oversized_files = [
                    f.name for f in uploaded_files if (len(f.getbuffer()) / (1024 * 1024)) > 50
                ]
                if oversized_files:
                    st.error(f"❌ Files exceed 50MB: {', '.join(oversized_files)}")
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