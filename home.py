









import streamlit as st
import pandas as pd
from user_db import create_users_table, add_user, validate_user, user_exists
import time 


create_users_table()

st.title("🔐 Login / Register System")

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "role" not in st.session_state:
    st.session_state["role"] = "user"


st.markdown(
    """
    <style>
    .scrollable-container {
        max-height: 600px;
        overflow-y: scroll;
        padding-right: 10px;
        border: 1px solid #ccc;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------ Register ------------------
if menu == "Register":
    st.subheader("Create a New Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    if st.button("Register"):
        if new_user and new_pass:
            if user_exists(new_user):
                st.warning("Username already exists!")
            else:
                add_user(new_user, new_pass)
                st.success("Registered successfully!")
        else:
            st.warning("Please enter both username and password.")

# ------------------ Login ------------------
elif menu == "Login":
    st.subheader("Login to Your Account")
    user = st.text_input("Username")
    passwd = st.text_input("Password", type="password")
    if st.button("Login"):
        role = validate_user(user, passwd)
        if role:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.session_state.role = role
            st.success("Login Successful!")
            
            time.sleep(1)
            st.switch_page("pages/dashboard.py")

            
            
        

        else:
            st.error("Incorrect username or password.")









