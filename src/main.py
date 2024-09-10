import os
import json

import streamlit as st
from groq import Groq

# Configurações da página streamlit
st.set_page_config(
    page_title="CrowAI GPT",
    page_icon="src/assets/crow_icon-bg.png",
    layout="centered"
)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]

# Salvar a chave da api para variável de ambiente
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# Inicializar o histórico de chat como estado de sessão não presente no streamlit
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Título da página do streamlit
st.title("CrowAI ChatBot")

# Mostrar histórico do chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de input para mensagem do usuário
user_prompt = st.chat_input("Pergunte à Crow...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Enviar a mensagem do usuário para a LLM e receber a resposta
    messages = [
        {"role": "system", "content": "You are a helpful assistant!"},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Mostrar a resposta da LLM
    with st.chat_message("assistant"):
        st.markdown(assistant_response)