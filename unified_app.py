import streamlit as st

if "plan" not in st.session_state:
    st.session_state.plan = "free"  # default to free

st.title("🎛️ Buzzstore File Renamer Launcher")
plan_choice = st.radio("Select your plan", ["Free Plan", "Premium Plan"], index=0 if st.session_state.plan=="free" else 1)
st.session_state.plan = "free" if plan_choice.startswith("Free") else "premium"

# Import the selected app
if st.session_state.plan == "free":
    import free_app
else:
    import premium_app