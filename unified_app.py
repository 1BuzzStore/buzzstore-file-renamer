import streamlit as st
import free_app
import premium_app

# ---------------------------
# Launcher
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.plan = "free"

st.title("Buzzstore File Renamer Launcher")

# --- LOGIN ---
if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    plan_option = st.radio("Plan", ["Free", "Premium"])

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.plan = plan_option.lower()
            st.experimental_rerun()  # reload page after login
        else:
            st.error("Please enter username and password")

# --- MAIN APP ---
else:
    plan = st.session_state.plan
    st.subheader(f"Welcome {plan.capitalize()} user!")

    if plan == "free":
        st.info("You are on Free Plan")
        free_app.run()  # Call free app function
        if st.button("Switch to Premium"):
            st.session_state.plan = "premium"
            st.experimental_rerun()
    else:
        st.success("You are on Premium Plan")
        premium_app.run()  # Call premium app function
        if st.button("Switch to Free"):
            st.session_state.plan = "free"
            st.experimental_rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.plan = "free"
        st.experimental_rerun()