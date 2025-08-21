import streamlit as st

# ---------- CONFIG ----------
FREE_MAX_UPLOAD_MB = 50
PREMIUM_MAX_UPLOAD_MB = 200

# Simulated user database: username -> plan
USER_DB = {
    "alice": "free",
    "bob": "premium",
    "charlie": "free"
}

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.plan = "free"
    st.session_state.username = ""

# ---------- LOGIN ----------
st.title("Buzzstore File Renamer")

if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")  # For demo only
    plan_option = st.radio("Plan", ["Free", "Premium"])

    if st.button("Login"):
        if username and password:
            if username in USER_DB:
                actual_plan = USER_DB[username]
                if plan_option.lower() != actual_plan:
                    st.error(f"This user has a {actual_plan.capitalize()} plan. Please select the correct plan.")
                else:
                    # Save login info in session
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.plan = actual_plan
                    st.query_params = {}
                    st.experimental_rerun() if hasattr(st, "experimental_rerun") else st.stop()
            else:
                st.error("Username not found")
        else:
            st.error("Please enter username and password")

# ---------- MAIN APP ----------
else:
    username = st.session_state.username
    plan = st.session_state.plan
    st.subheader(f"Welcome {username} ({plan.capitalize()} Plan)")

    # Restrict max upload size based on plan
    max_size_mb = FREE_MAX_UPLOAD_MB if plan == "free" else PREMIUM_MAX_UPLOAD_MB
    st.info(f"Your max upload size is {max_size_mb}MB per file")

    uploaded_file = st.file_uploader("Drag and drop file here", type=["*"], key="uploader")
    if uploaded_file:
        if uploaded_file.size > max_size_mb * 1024 * 1024:
            st.error(f"File too large! Max {max_size_mb}MB allowed for {plan.capitalize()} plan.")
        else:
            st.success(f"{uploaded_file.name} uploaded successfully!")

    # ---------- LOGOUT ----------
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.plan = "free"
        st.query_params = {}
        st.experimental_rerun() if hasattr(st, "experimental_rerun") else st.stop()