import sys, os
sys.path.append(os.getcwd())

import streamlit as st
from utils import APIClient

# Streamlit interface
st.title("Gamestop sales assistant")

if st.sidebar.button('Reset Chat'):
    APIClient.reset_chat()
    st.session_state["messages"] = []
    st.session_state.messages.append({"role": "assistant", "content": APIClient.root()['response']})

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": APIClient.root()['response']})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = APIClient.chat(prompt)['response']
        st.write(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

