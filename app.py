import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

# Url = app-form-benyxxbxau4q6xvprzhjpq.streamlit.app

# Configuración de autenticación con Google Sheets usando google-auth
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]

# leer las credenciales desde secrets (Streamlit Cloud)
service_account_info = st.secrets["gcp_service_account"]
credentials = Credentials.from_service_account_info(service_account_info)
client = gspread.authorize(credentials)

# Abrir la hoja de Google Sheets
SHEET_NAME = "prueba_streamlit"
sheet = client.open(SHEET_NAME).sheet1

# Estructura Formulario
st.title("Formulario de Registro de Costos")
descripcion = st.text_input("Descripción del Gasto")
monto = st.number_input("Monto del Gasto", min_value=0.0, format="%.2f")
item = st.selectbox("Ítem", ['Aseo y Ornato', 'Choclo', 'Frambuesas', 'Papas', 'Pasto', 'Peonías', 'Campo General'])

if st.button("Guardar Registro"):
    sheet.append_row([descripcion, monto, item])
    st.success("¡Registro guardado con éxito!")