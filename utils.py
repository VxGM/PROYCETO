import streamlit as st
import os

def cargar_css():
    with open("templates/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
