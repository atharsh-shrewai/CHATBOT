import streamlit as st 
import requests

BACKEND_URL = "https://18-196-60-180.nip.io/chat"

# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="centered"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# App title
st.title("🤖 AI Chat Assistant")
st.caption("Ask me anything!")

# Display chat messages in a container
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat input at the bottom
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with chat_container:
        with st.chat_message("user"):
            st.write(user_input)
    
    # Get response from backend
    with chat_container:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    payload = {"question": user_input}
                    response = requests.post(BACKEND_URL, json=payload)
                    
                    if response.status_code == 200:
                        bot_response = response.json().get("response", "No response received.")
                    else:
                        bot_response = f"Error: Unable to get response (Status: {response.status_code})"
                except Exception as e:
                    bot_response = f"Error: {str(e)}"
                
                st.write(bot_response)
    
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # Rerun to update the chat
    st.rerun()

# Sidebar with options
with st.sidebar:
    st.header("Options")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.caption(f"💬 Total messages: {len(st.session_state.messages)}")
