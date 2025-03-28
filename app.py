import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

# Configuración de autenticación con Google Sheets usando google-auth
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file"
]

# Autenticación y conexión con Google Sheets
try:
    # Leer las credenciales desde secrets (Streamlit Cloud)
    service_account_info = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPE)
    client = gspread.authorize(credentials)
    st.write("✅ Conexión autenticada exitosamente con Google Sheets")
except Exception as e:
    st.error(f"❌ Error en la autenticación con Google Sheets: {e}")

# Intentar abrir la hoja de Google Sheets
SHEET_NAME = "prueba_streamlit"
try:
    sheet = client.open(SHEET_NAME).sheet1
    st.write(f"✅ Hoja de Google Sheets '{SHEET_NAME}' abierta exitosamente")
except Exception as e:
    st.error(f"❌ Error al abrir la hoja de Google Sheets: {e}")

# Estructura del Formulario
st.title("Formulario de Registro de Costos")
descripcion = st.text_input("Descripción del Gasto")
monto = st.number_input("Monto del Gasto", min_value=0.0, format="%.2f")
item = st.selectbox("Ítem", ['Aseo y Ornato', 'Choclo', 'Frambuesas', 'Papas', 'Pasto', 'Peonías', 'Campo General'])

if st.button("Guardar Registro"):
    try:
        # Intentar guardar los datos en la hoja
        sheet.append_row([descripcion, monto, item])
        st.success("¡Registro guardado con éxito!")
    except Exception as e:
        st.error(f"❌ Error al guardar el registro en Google Sheets: {e}")
