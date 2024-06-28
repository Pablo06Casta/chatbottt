import streamlit as st
from chatbot import predict_class, get_response

st.sidebar.title("Opciones")

# Definir los enlaces a las páginas web en un desplegable
selected_option = st.sidebar.selectbox(
    "Selecciona una opción:",
    ["Google", "OpenAI", "GitHub"]
)

# Diccionario de enlaces a las páginas web
options = {
    "Google": "https://www.google.com",
    "OpenAI": "https://www.openai.com",
    "GitHub": "https://www.github.com"
}

# Redirigir al usuario cuando seleccione una opción
if selected_option in options:
    st.sidebar.markdown(f"Redireccionando a [{selected_option}]({options[selected_option]})")


st.title("Asistente Virtual")

# Inicialización de la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True

# Mostrar mensajes existentes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Mensaje inicial del asistente
if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?")
    st.session_state.messages.append({"role": "assistant", "content": "Hola, ¿cómo puedo ayudarte?"})
    st.session_state.first_message = False

# Manejo de mensajes del usuario
if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Obtener respuesta del chatbot
    insts = predict_class(prompt)
    res = get_response(insts)

    # Mostrar respuesta del chatbot
    with st.chat_message("assistant"):
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

