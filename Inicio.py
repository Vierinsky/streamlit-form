import gspread
from google.oauth2.service_account import Credentials
import json
import os
import streamlit as st

st.set_page_config(page_title="Registro de Costos e Ingresos", layout="centered")

tab1, tab2 = st.tabs(["📊 Vista General", "🧾 Formularios"])

with tab1:
    # Aquí los gráficos, KPIs, tablas

with tab2:
    st.page_link("pages/1 Formulario de Costos.py", label="Formulario de Costos")
    st.page_link("pages/2 Formulario de Ingresos.py", label="Formulario de Ingresos")


st.title("Bienvenido al Sistema de Registro")

st.subheader("Selecciona una opción para comenzar:")

# Botón para ir a Formulario de Costos
if st.button("Ir a Formulario de Costos"):
    st.switch_page("pages/1 Formulario de Costos.py")

# Botón para ir a Formulario de Ingresos
if st.button("Ir a Formulario de Ingresos"):
    st.switch_page("pages/2 Formulario de Ingresos.py")

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
