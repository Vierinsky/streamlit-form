import gspread
from google.oauth2.service_account import Credentials
import json
import os
import streamlit as st

st.set_page_config(page_title="Registro de Costos e Ingresos", layout="centered")

st.title("Bienvenido al Sistema de Registro")
st.subheader("Seleccione una Página:")

col1, col2, col3, col4, col5 = st.columns(5)

button_style = """
    <style>
    div.stButton > button {
        width: 100%;
    }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)

with col1:
    if st.button("Reporte: Costos v/s Ingresos"):
        st.switch_page("pages/1 Reporte General.py")

with col2:
    if st.button("Formulario de Compras"):
        st.switch_page("pages/2 Formulario de Compras.py")

with col3:
    if st.button("Formulario de Sueldos"):
        st.switch_page("page/3 Formulario de Sueldos.py")

with col4:
    if st.button("Formulario de Ingresos"):
        st.switch_page("pages/4 Formulario de Ingresos.py") 

with col5:
    if st.button("Vencimientos Pendientes"):
        st.switch_page("pages/5 Vencimientos Pendientes.py")

# Configuración de autenticación con Google Sheets usando google-auth
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Intentar abrir la hoja de Google Sheets
SHEET_NAME = "prueba_streamlit"             # ⚠️Modificar en producción⚠️

# Autenticación y conexión con Google Sheets
try:
    service_account_info = json.loads(os.environ["GCP_SERVICE_ACCOUNT"])             # ⚠️Modificar en producción⚠️
    credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPE)
    client = gspread.authorize(credentials)
    spreadsheet = client.open(SHEET_NAME)

    # Guardar en sesión para que esté accesible en otras páginas
    st.session_state["spreadsheet"] = spreadsheet

    # Mostrar estado en la barra lateral
    with st.sidebar:
        with st.expander("🔧 Estado de conexión", expanded=False):
            st.success("✅ Conexión con Google Sheets exitosa")
            st.success(f"✅ Hoja activa: '{SHEET_NAME}'")

except Exception as e:
    st.sidebar.error("❌ Falló la conexión con Google Sheets")
    st.stop()