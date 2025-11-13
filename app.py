import streamlit as st
from openai import OpenAI
import os

# Load API key from environment variable for security
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OPENAI_API_KEY is not set. Please add it in your environment variables.")
else:
    client = OpenAI(api_key=api_key)

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Education Chatbot")

st.write("Ask me anything related to your school subjects, and I’ll explain it clearly!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]]:
        st.write(msg["content"])

# User input
prompt = st.chat_input("Type your question...")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Call OpenAI API
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a helpful school tutor."}] +
                         st.session_state.messages
            )

            reply = response.choices[0].message.content
            st.write(reply)

            # Save assistant message
            st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"API error: {e}")