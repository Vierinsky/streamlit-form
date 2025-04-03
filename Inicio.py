import gspread
from google.oauth2.service_account import Credentials
import json
import os
import streamlit as st

st.set_page_config(page_title="Registro de Costos e Ingresos", layout="centered")

st.title("Bienvenido al Sistema de Registro")

st.subheader("Selecciona una opción para comenzar:")

# Botón para ir a Formulario de Costos
if st.button("Ir a Formulario de Costos"):
    st.switch_page("pages/1_Formulario_Costos.py")

# Botón para ir a Formulario de Ingresos
if st.button("Ir a Formulario de Ingresos"):
    st.switch_page("pages/2_Formulario_Ingresos.py")

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

    # ✅ Mostrar estado en expander discreto
    with st.expander("🔧 Estado de conexión (click para ver)", expanded=False):
        st.success("✅ Conexión autenticada exitosamente con Google Sheets")
        st.success(f"✅ Hoja de Google Sheets '{SHEET_NAME}' abierta exitosamente")

    # Guardar en sesión para que esté accesible en otras páginas
    st.session_state["spreadsheet"] = spreadsheet

except Exception as e:
    st.error(f"❌ Error de conexión con Google Sheets: {e}")
