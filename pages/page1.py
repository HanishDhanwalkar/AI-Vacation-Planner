from navigation import make_sidebar
import streamlit as st

# import streamlit_app

make_sidebar()

with open("tmp/tmp.txt") as f:
    username = f.read()

st.write(
    f"""
Welcome {username} to the secret stuff.

Hello
"""
)