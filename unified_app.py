import streamlit as st
import os
import io
import zipfile

# ---------------------------
# Simple User Database
# ---------------------------
# Replace with your real authentication method
USERS = {
    "freeuser": {"password": "free123", "plan": "free"},
    "premiumuser": {"password": "premium123", "plan": "premium"}
}

# ---------------------------
# Login Section
# ---------------------------
st.title("🔑 File Renamer Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.plan = USERS[username]["plan"]
            st.success(f"Welcome {username}! You are on the {st.session_state.plan.capitalize()} plan.")
        else:
            st.error("❌ Invalid credentials")
else:
    # ---------------------------
    # Determine plan limits
    # ---------------------------
    plan = st.session_state.plan

    if plan == "free":
        st.subheader("🆓 Free File Renamer")
        st.info("📦 Free Plan: Upload up to **5 files**, max **50MB each**")
        max_files = 5
        max_size_mb = 50
    else:
        st.subheader("💎 Premium File Renamer")
        st.success("💎 Premium Plan: Unlimited files, max **200MB each**")
        max_files = None
        max_size_mb = 200

    # ---------------------------
    # File Upload Section
    # ---------------------------
    uploaded_files = st.file_uploader(
        f"Upload files to rename (Max {'5 files' if plan=='free' else 'unlimited'}, {max_size_mb}MB each)",
        accept_multiple_files=True
    )

    prefix = st.text_input("Enter prefix for renamed files", value="buzzstore")

    if st.button("Rename Files"):
        if uploaded_files:
            # Check file count for free users
            if plan == "free" and len(uploaded_files) > max_files:
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
                    # Create ZIP
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

    # ---------------------------
    # Logout
    # ---------------------------
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()