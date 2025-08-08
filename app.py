import streamlit as st
from db_config.db import obtener_conexion
from db_config.db import autenticar_pasajero
from Core.Servicios import registro, reserva, resumen, bitacora, admin_pasajero
from Core.Servicios.bitacora import registrar_salida,registrar_inicio
import socket
from PIL import Image
import os

def mostrar_bienvenida():
    st.markdown("""
        <h1>✈️ Bienvenido a <span style='color:#1f77b4'>SkyWings</span></h1>
        <p>Reserva tus vuelos de forma rápida, segura y confiable.</p>
    """, unsafe_allow_html=True)

    ruta_imagen = os.path.join("static", "avion_horizontal.png")
    imagen = Image.open(ruta_imagen)
    st.image(imagen, use_container_width=True)

def mostrar_login():
    st.header("🔐 Iniciar sesión")
    correo = st.text_input("📧 Correo electrónico")
    password = st.text_input("🔒 Contraseña", type="password")

    if st.button("Entrar", key="btn_login"):
        usuario = autenticar_pasajero(correo, password)
        if usuario:
            st.session_state.usuario = usuario
            registrar_inicio(usuario["nombre"])
            st.session_state.opcion_actual = None
            st.success(f"✅ Bienvenido {usuario['nombre']} ({usuario['rol']})")
        else:
            st.error("📛 Correo no registrado.")

def mostrar_menu():
    opciones = []
    usuario = st.session_state.get("usuario", None)

    if usuario:
        if usuario["rol"] == "admin":
            opciones = ["Reservar vuelo", "Registrar pasajero", "Administrar Pasajeros" , "Ver resumen", "Bitácora", "Cerrar sesión"]
        elif usuario["rol"] == "usuario":
            opciones = ["Reservar vuelo", "Cerrar sesión"]
        else:
            opciones = ["Cerrar sesión"]
    else:
        opciones = ["Iniciar sesión", "Registrar pasajero"]

    cols = st.columns(len(opciones))
    for i, opcion in enumerate(opciones):
        if cols[i].button(opcion):
            st.session_state.opcion_actual = opcion

# --- App Principal ---
def main():
    st.set_page_config(page_title="SkyWings", page_icon="✈️")
    if "ip" not in st.session_state:
        try:
            st.session_state.ip = socket.gethostbyname(socket.gethostname())
        except:
            st.session_state.ip = "127.0.0.1"

    if "user_agent" not in st.session_state:
        st.session_state.user_agent = "Desconocido" 
    if "usuario" not in st.session_state:
        st.session_state.usuario = None
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = None
    

    mostrar_menu()

    opcion = st.session_state.opcion_actual
    usuario = st.session_state.usuario
    
    if opcion == "Iniciar sesión":
        mostrar_login()

    elif opcion == "Registrar pasajero":
        registro.mostrar()

    elif opcion == "Reservar vuelo":
        if usuario:
            reserva.mostrar(usuario)
        else:
            st.warning("⚠️ Debes iniciar sesión.")
            
    elif opcion == "Administrar Pasajeros":
        if usuario and usuario["rol"] == "admin":
            admin_pasajero.mostrar()
        else:
            st.error("⛔ Acceso denegado. Solo administradores pueden acceder.")

    elif opcion == "Listado de pasajeros":
        if usuario and usuario["rol"] == "admin":
            registro.mostrar()
        else:
            st.error("⛔ Acceso denegado. Solo administradores pueden ver esta sección.")

    elif opcion == "Ver resumen":
        if usuario:
            resumen.mostrar()
        else:
            st.warning("⚠️ Debes iniciar sesión.")
            
    elif opcion == "Bitácora":
        if usuario and usuario["rol"] == "admin":
            bitacora.mostrar()
        else:
            st.error("⛔ Acceso denegado. Solo administradores pueden ver la bitácora.")
        
    elif opcion == "Cerrar sesión":
        registrar_salida(st.session_state.usuario["nombre"])
        st.session_state.usuario = None
        st.session_state.opcion_actual = None
        st.success("👋 Has cerrado sesión.")

    else:
        mostrar_bienvenida()
       

if __name__ == "__main__":
    main()