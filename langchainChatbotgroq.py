from langchain_groq import ChatGroq as Groq
import streamlit as st
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Your Friendly Chatbot",
    page_icon="🤖",
    layout="centered" 
)
st.title("Hello there! How can I assist you today? 🤖")

parser = StrOutputParser()
llm = Groq(model="llama-3.1-8b-instant", temperature=0)

# Init session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ("system", "You are a helpful chat assistant.")
    ]

# 🔹 Render messages
for role, msg in st.session_state.chat_history:
    if role != "system":
        with st.chat_message(role):
            st.markdown(msg)

# 🔹 Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    prompt = ChatPromptTemplate.from_messages(st.session_state.chat_history)
    chain = prompt | llm | parser
    response = chain.invoke({})

    st.session_state.chat_history.append(("assistant", response))

    # Rerun to immediately render response
    st.rerun()

