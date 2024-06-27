import streamlit as st
from chatbot import predict_class, get_response, intents
import openai # Asegúrate de importar openai correctamente
from call_chatgpt import call_chatgpt  # Asegúrate de importar call_chatgpt correctamente

st.title("Asistente Virtual")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte?")
    st.session_state.messages.append({"role": "assistant", "content": "Hola, ¿cómo puedo ayudarte?"})
    st.session_state.first_message = False

if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    insts = predict_class(prompt)
    res = get_response(insts)

    if res == "ChatGPT":
        chatgpt_response = call_chatgpt(prompt)

        with st.chat_message("assistant"):
            st.markdown("ChatGPT: " + chatgpt_response)
    else:
        with st.chat_message("assistant"):
            st.markdown(res)

    st.session_state.messages.append({"role": "assistant", "content": res})
