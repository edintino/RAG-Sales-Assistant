import sys
import os
sys.path.append(os.getcwd())

import streamlit as st
from utils import APIClient

# Streamlit interface
st.title("RAG Sales Assistant Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

def add_message(role, content):
    st.session_state["messages"].insert(0, {"role": role, "content": content})  # Insert at the beginning

# Function to call the chat API
def chat_api(user_input):
    # Dummy response for demonstration; replace with actual API call
    return {"response": f"Assistant's response to '{user_input}'"}

# Input area
with st.form(key='chat_form', clear_on_submit=True):  # clear_on_submit clears the text box
    user_input = st.text_input("You: ", "")
    submit_button = st.form_submit_button(label='Send')

if submit_button and user_input:
    add_message("user", user_input)
    try:
        response = chat_api(user_input)
        add_message("assistant", APIClient.chat(user_input)['response'])
    except Exception as e:
        add_message("assistant", str(e))

if st.button('Reset Chat'):
    APIClient.reset_chat()
    st.session_state["messages"] = []

# Display chat messages
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f"<div style='text-align: right; background-color: #0084ff; color: white; padding: 10px; border-radius: 5px; max-width: 60%; margin-left: auto;'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color: #e5e5ea; padding: 10px; border-radius: 5px; max-width: 60%;'>{message['content']}</div>", unsafe_allow_html=True)
