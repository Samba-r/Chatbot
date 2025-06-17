import streamlit as st
from groq import Groq
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

st.set_page_config(page_title="SambaIA")
st.title("Bienvenidos a la mejor IA")

def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def crear_cliente_groq():
    groq_api_key = "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"
    return Groq(api_key=groq_api_key)

def mostrar_sidebar():
    st.sidebar.title("¿Con quien querés hablar?")
    modelo = st.sidebar.selectbox('Elegí tu esclavo:', MODELOS, index=0)
    return modelo

def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

def agregar_mensajes_previos(role, content):
    st.session_state.mensajes.append({"role": role, "content": content})

def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream=False
    )
    return respuesta.choices[0].message.content

def ejecutar_chat():
    inicializar_estado_chat()
    cliente = crear_cliente_groq()
    modelo = mostrar_sidebar()

    for mensaje in st.session_state.mensajes:
        mostrar_mensaje(mensaje["role"], mensaje["content"])

    mensaje_usuario = st.chat_input("Mandale nomás")

    if mensaje_usuario:
        agregar_mensajes_previos("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)

        respuesta_contenido = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)

        agregar_mensajes_previos("assistant", respuesta_contenido)
        mostrar_mensaje("assistant", respuesta_contenido)

if __name__ == '__main__':
    ejecutar_chat()
