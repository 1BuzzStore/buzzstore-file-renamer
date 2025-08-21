import streamlit as st

st.title("Buzzstore File Renamer Launcher")
st.subheader("Choose Your Plan")

st.info("🔹 Free Plan: up to 5 files, 50MB each\n🔹 Premium Plan: unlimited files, 200MB each")

st.write("Click below to open the app in a new tab:")

# Buttons to open the separate apps
st.markdown("[🆓 Open Free Plan](http://localhost:8502)", unsafe_allow_html=True)
st.markdown("[💎 Open Premium Plan](http://localhost:8503)", unsafe_allow_html=True)