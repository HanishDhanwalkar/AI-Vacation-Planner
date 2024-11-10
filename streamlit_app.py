import streamlit as st
from time import sleep
import os
from navigation import make_sidebar

if os.path.exists('tmp/tmp.txt'):
    os.remove('tmp/tmp.txt')
    
make_sidebar()

st.title("AI Travel Planner Bot")

st.write("Please log in to continue (username `test`, password `test`).")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

def get_username():
    return username

if st.button("Log in", type="primary"):
    if username == "test" and password == "test":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        
        with open('tmp/tmp.txt', "w") as f:
            f.write(username)
            
        sleep(0.5)
        st.switch_page("pages/page1.py")
    else:
        st.error("Incorrect username or password")