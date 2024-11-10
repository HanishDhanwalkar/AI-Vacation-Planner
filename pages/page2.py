from navigation import make_sidebar
import streamlit as st
import os

import ollama
from typing import Dict, Generator

import pandas as pd

make_sidebar()

with open("tmp/tmp.txt") as f:
    username = f.read()
    
if os.path.exists(f'tmp/{username}.csv'):
    print("Loaded previous history")
    df = pd.read_csv(f'tmp/{username}.csv')
else:
    df = pd.DataFrame(columns=['role', 'content'])
SYS_MSG = """You are a one-day tour planning assistant that helps users create a comprehensive plan for exploring a city based on their preferences. The system should remember user preferences across the conversation to personalize future itinerary suggestions based on past interactions. 

As an professional travel assistant you must:
1. Ask the user for details such as the city to visit, available timings, budget, and interests (e.g., culture, adventure, food, shopping).
2. Ask for a starting point, such as their hotel or any other location. If the user does not provide a starting point, consider the starting point to be the first attraction itself. Include the distance and travel time from the starting point to the first attraction if a starting point is provided.
3. If the user is unsure about what places to visit or their preferences, suggest popular attractions based on the city, user interests, and budget.

Ask this questions in converstions one by one. And not bombard them with list of question. Ask only one question at a time.

Ask about dates and duration for which itinerary needs to be planned first.

Based on the user's preferences, you should generate an itinerary that includes 
the following details:
1. A list of places to visit,
2. the optimal sequence of visits,
3. transportation methods. 
"""


MESSAGES = []
for role, content in zip(df['role'], df['content']):
        MESSAGES.append({"role": role, "content": [content]})
        
def ollama_generator(model_name: str, msgs: Dict) -> Generator:
    system_message = SYS_MSG
    
    messages = []
    messages.append({"role": "system", "content": system_message})
    for role, content in zip(df['role'], df['content']):
        messages.append({"role": role, "content": content})
        if role == 'user':
            messages.append({"role": "system", "content": system_message})
    
    stream = ollama.chat(
        model=model_name, messages=msgs, stream=True)
    for chunk in stream:
        yield chunk['message']['content']
        
def create_iter(model_name: str) -> Generator:
    msgs = []
    for role, content in zip(df['role'], df['content']):
        msgs.append({"role": role, "content": content})
    msgs.append({"role": "User", "content": "Create a travel iterary for me based on previous conversation"})
    
    stream = ollama.chat(
        model=model_name, messages=msgs, stream=True
    )
    for chunk in stream:
        yield chunk['message']['content']
    
    
st.title("Ollama with Streamlit demo")
if "selected_model" not in st.session_state:
    st.session_state.selected_model = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
    for role, content in zip(df['role'], df['content']):
        st.session_state.messages.append({"role": role, "content": content})
    
    
st.session_state.selected_model = st.selectbox(
    "Please select the model:", [model["name"] for model in ollama.list()["models"]])
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("How could I help you?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        MESSAGES.append({"role": "user", "content": prompt})
        
        

    with st.chat_message("assistant"):
        response = st.write_stream(ollama_generator(
            st.session_state.selected_model, st.session_state.messages))
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
    MESSAGES.append({"role": "assistant", "content": response})
    
    
    df = pd.DataFrame(MESSAGES, columns=['role', 'content'])
    df.to_csv(f'tmp/{username}.csv', index=False)
    print('history saved')

if st.button('Create iterary'):
    st.write(create_iter(st.session_state.selected_model))