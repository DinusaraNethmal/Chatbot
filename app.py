import streamlit as st
from google import genai
from google.genai import types
import sys

st.set_page_config(
    page_title="My Chatbot",
    page_icon="🤖",
    layout="centered",
)

@st.cache_resource
def load_client():
    try:
        return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    except KeyError:
        st.error("❌ API Key not found. Please check .streamlit/secrets.toml")
        return None

client = load_client()

# Stop the app if no key is found
if client is None:
    st.stop()

def get_chat_session():
    return client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful AI assistant."
        )
    )

# --- Session State Management ---
if "chat" not in st.session_state:
    st.session_state.chat = get_chat_session()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- The App UI ---
st.title("My Chatbot 🤖")
st.markdown("""
    Welcome! I am an AI chatbot ready to help you. 
    Ask me anything about **coding, science, writing, or general knowledge**.
""")

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle Input
if user_prompt := st.chat_input("What's up?"):
    
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("model"):
        with st.spinner("Thinking..."):  
            try:
                # Send message to Gemini
                response = st.session_state.chat.send_message(user_prompt)
                bot_response = response.text
            except Exception as e:
                bot_response = f"❌ Error: {e}"
        
        st.markdown(bot_response)

    st.session_state.messages.append({"role": "model", "content": bot_response})