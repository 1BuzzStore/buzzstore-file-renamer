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
PREMIUM_PASSWORD = "buzzpremium"  # change this to your desired premium key

# ---------------------------
# SESSION STATE
# ---------------------------
if "plan" not in st.session_state:
    st.session_state.plan = "free"
if "view" not in st.session_state:
    st.session_state.view = "free"
if "exceeded_limits" not in st.session_state:
    st.session_state.exceeded_limits = False
if "premium_authenticated" not in st.session_state:
    st.session_state.premium_authenticated = False

# ---------------------------
# FUNCTIONS
# ---------------------------
def rename_files(uploaded_files, prefix, max_mb):
    oversized_files = [
        f.name for f in uploaded_files if (len(f.getbuffer()) / (1024 * 1024)) > max_mb
    ]
    if oversized_files:
        st.error(
            f"❌ The following files exceed the {max_mb}MB limit: {', '.join(oversized_files)}"
        )
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
# FREE PLAN VIEW
# ---------------------------
st.title("📝 Buzzstore File Renamer")
st.subheader("🆓 Free File Renamer")
st.info(f"Upload up to {FREE_MAX_FILES} files, max {FREE_MAX_MB}MB each")

uploaded_files = st.file_uploader(
    f"Upload files (Max {FREE_MAX_FILES} files, {FREE_MAX_MB}MB each)",
    accept_multiple_files=True
)
prefix = st.text_input("Enter prefix for renamed files", value="buzzstore_free")

if st.button("Rename Files (Free)"):
    if uploaded_files:
        # Check if user exceeded free limits
        if len(uploaded_files) > FREE_MAX_FILES or any(
            (len(f.getbuffer()) / (1024 * 1024)) > FREE_MAX_MB for f in uploaded_files
        ):
            st.session_state.exceeded_limits = True
            st.warning("⚠️ You've exceeded Free plan limits!")
        else:
            rename_files(uploaded_files, prefix, FREE_MAX_MB)
    else:
        st.warning("⚠️ Please upload at least one file.")

# ---------------------------
# PREMIUM AUTHENTICATION
# ---------------------------
if st.session_state.exceeded_limits and not st.session_state.premium_authenticated:
    st.subheader("💎 Upgrade to Premium")
    st.info(f"Unlimited files, max {PREMIUM_MAX_MB}MB each")
    
    premium_key = st.text_input("Enter Premium Key to access Premium features", type="password")
    if st.button("Authenticate Premium"):
        if premium_key == PREMIUM_PASSWORD:
            st.session_state.premium_authenticated = True
            st.success("✅ Premium Access Granted!")
        else:
            st.error("❌ Invalid Premium Key")

# ---------------------------
# PREMIUM UPLOADER (After Authentication)
# ---------------------------
if st.session_state.premium_authenticated:
    st.subheader("💎 Premium File Renamer")
    premium_uploaded_files = st.file_uploader(
        f"Upload files (Max {PREMIUM_MAX_MB}MB each)",
        accept_multiple_files=True,
        key="premium_uploader"
    )
    premium_prefix = st.text_input(
        "Enter prefix for renamed files (Premium)",
        value="buzzstore_premium",
        key="premium_prefix"
    )

    if st.button("Rename Files (Premium)"):
        if premium_uploaded_files:
            rename_files(premium_uploaded_files, premium_prefix, PREMIUM_MAX_MB)
        else:
            st.warning("⚠️ Please upload at least one file.")