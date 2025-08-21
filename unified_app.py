import streamlit as st
import os
import io
import zipfile

# ---------------------------
# PLAN CONFIG
# ---------------------------
FREE_MAX_FILES = 5
FREE_MAX_MB = 50
PREMIUM_MAX_MB = 200
PREMIUM_PASSWORD = "buzzpremium"  # change to your desired premium key

# ---------------------------
# SESSION STATE
# ---------------------------
if "view" not in st.session_state:
    st.session_state.view = "free"
if "premium_authenticated" not in st.session_state:
    st.session_state.premium_authenticated = False
if "exceeded_limits" not in st.session_state:
    st.session_state.exceeded_limits = False

# ---------------------------
# HELPER FUNCTION
# ---------------------------
def rename_files(uploaded_files, prefix, max_mb):
    oversized_files = [
        f.name for f in uploaded_files if (len(f.getbuffer()) / (1024 * 1024)) > max_mb
    ]
    if oversized_files:
        st.error(f"❌ The following files exceed {max_mb}MB: {', '.join(oversized_files)}")
        return False

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

    if st.button("Rename Files (Free)"):
        if uploaded_files:
            if len(uploaded_files) > FREE_MAX_FILES or any(
                (len(f.getbuffer()) / (1024 * 1024)) > FREE_MAX_MB for f in uploaded_files
            ):
                st.session_state.exceeded_limits = True
                st.experimental_rerun()  # <-- removed in new version
            else:
                rename_files(uploaded_files, prefix, FREE_MAX_MB)

    if st.session_state.exceeded_limits:
        st.warning("⚠️ You've exceeded Free plan limits!")
        # Single-click button effect
        if st.button("Apply for Premium 💎"):
            st.session_state.view = "premium_login"
            st.session_state.exceeded_limits = False  # reset
            st.stop()  # immediately refresh layout

# ---------------------------
# PREMIUM LOGIN VIEW
# ---------------------------
elif st.session_state.view == "premium_login":
    st.title("💎 Premium Access Required")
    st.info(f"Unlimited files, max {PREMIUM_MAX_MB}MB each")

    premium_key = st.text_input("Enter Premium Key", type="password")
    if st.button("Authenticate Premium"):
        if premium_key == PREMIUM_PASSWORD:
            st.session_state.premium_authenticated = True
            st.session_state.view = "premium"
        else:
            st.error("❌ Invalid Premium Key")

    if st.button("← Back to Free"):
        st.session_state.view = "free"
        st.session_state.exceeded_limits = False
        st.stop()

# ---------------------------
# PREMIUM VIEW
# ---------------------------
elif st.session_state.view == "premium" and st.session_state.premium_authenticated:
    st.title("💎 Premium File Renamer")
    st.success(f"Unlimited files, max {PREMIUM_MAX_MB}MB each")

    premium_uploaded_files = st.file_uploader(
        f"Upload files (Max {PREMIUM_MAX_MB}MB each)",
        accept_multiple_files=True,
        key="premium_uploader"
    )
    premium_prefix = st.text_input("Enter prefix for renamed files (Premium)", value="buzzstore_premium")

    if st.button("Rename Files (Premium)"):
        if premium_uploaded_files:
            rename_files(premium_uploaded_files, premium_prefix, PREMIUM_MAX_MB)
        else:
            st.warning("⚠️ Please upload at least one file.")

    if st.button("← Back to Free"):
        st.session_state.view = "free"
        st.session_state.exceeded_limits = False
        st.stop()