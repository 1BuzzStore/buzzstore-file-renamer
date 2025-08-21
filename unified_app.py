import streamlit as st

# ---------- CONFIG ----------
FREE_MAX_UPLOAD_MB = 50
PREMIUM_MAX_UPLOAD_MB = 200

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.plan = "free"

# ---------- LOGIN ----------
st.title("Buzzstore File Renamer")

if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    plan_option = st.radio("Plan", ["Free", "Premium"])

    if st.button("Login"):
        # Here you can add real authentication
        if username and password:
            st.session_state.logged_in = True
            st.session_state.plan = plan_option.lower()  # "free" or "premium"
            st.success(f"Logged in as {username} ({plan_option} Plan)")
            st.experimental_set_query_params()  # reset query params
            st.stop()  # stop execution to reload page
        else:
            st.error("Please enter username and password")

# ---------- MAIN APP ----------
if st.session_state.logged_in:
    plan = st.session_state.plan
    st.subheader(f"Welcome {plan.capitalize()} user!")
    
    # Determine max upload size
    max_size_mb = FREE_MAX_UPLOAD_MB if plan == "free" else PREMIUM_MAX_UPLOAD_MB
    st.info(f"Your max upload size is {max_size_mb}MB per file")

    uploaded_file = st.file_uploader("Drag and drop file here", type=["*"], key="uploader")
    if uploaded_file:
        if uploaded_file.size > max_size_mb * 1024 * 1024:
            st.error(f"File too large! Max {max_size_mb}MB allowed for {plan} plan.")
        else:
            st.success(f"{uploaded_file.name} uploaded successfully!")

    # ---------- LOGOUT ----------
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.plan = "free"
        st.experimental_set_query_params()
        st.stop()  # reload page