import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Custom CSS
st.markdown("""
<style>
.stTextInput>div>div>input {
    border-radius: 8px;
}
.stButton>button {
    border-radius: 8px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 AI Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Show assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": m["role"], "content": m["content"]} 
                         for m in st.session_state.messages]
            )
            assistant_response = response.choices[0].message.content
            message_placeholder.markdown(assistant_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_response}
            )
        except Exception as e:
            message_placeholder.error(f"Error: {str(e)}")