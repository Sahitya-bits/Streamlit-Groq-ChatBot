import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
groq_api_key = os.getenv("groq_api_key")

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Sidebar - Personalization
st.sidebar.title("Personalization")

# System prompt - editable
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are a helpful assistant."

prompt = st.sidebar.text_area(
    "System Prompt:",
    value=st.session_state.system_prompt,
    height=100
)
st.session_state.system_prompt = prompt  # Keep updated

# Model selection
model = st.sidebar.selectbox(
    "Choose a model",
    ["Llama3-8b-8192", "deepseek-r1-distill-llama-70b", "qwen-qwq-32b", "gemma2-9b-it"]
)

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": st.session_state.system_prompt}
    ]

# Title
st.title("💬 ChatBot")

# User input
user_input = st.text_input("How can I help you?", "")

# Submit button
if st.button("Submit") and user_input:
    messages = st.session_state.history.copy()
    messages.append({"role": "user", "content": user_input})

    # Get model response
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )

    response = chat_completion.choices[0].message.content
    messages.append({"role": "assistant", "content": response})

    # Update session state
    st.session_state.history = messages

    # Display response
    st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)

# Sidebar - Chat History
st.sidebar.title("Previous Chats")

for i in range(1, len(st.session_state.history)):
    entry = st.session_state.history[i]

    if entry["role"] == "system":
        continue

    label = "👤" if entry["role"] == "user" else "🤖"
    prefix = "Query" if entry["role"] == "user" else "Response"
    display_text = f"{label} {prefix} {i//2+1}: {entry['content'][:30]}..."

    if st.sidebar.button(display_text, key=f"history_{i}"):
        st.markdown(f'<div class="response-box">{entry["content"]}</div>', unsafe_allow_html=True)
