# Formulario de Sueldos

# TODO:
#   - Leyes sociales:
#       - (Completar)
#   - Sueldo operario: El total de días trabajados se divide en distintos cultivos donde trabajó.
#                      Su sueldo se divide en esos días y se registra en el cultivo correspondiente.
#   - No se utiliza factura.
#   - Se suman gratificaciones (Transporte, Alimentación), las que se suman después de todos los descuentos. 

from google.oauth2.service_account import Credentials
import gspread
import json
import os
import pandas as pd
import streamlit as st

# === Configuración Google Sheets ===
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_NAME = "prueba_streamlit"  # ⚠️Modificar en producción⚠️

# === Funciones de Utilidad ===
def get_fresh_spreadsheet():
    """
    Devuelve una conexión activa a Google Sheets. Si ya existe en session_state, la reutiliza.

    Returns:
        gspread.Spreadsheet: conexión activa.
    """
    if "spreadsheet" not in st.session_state:
        service_account_info = json.loads(os.environ["GCP_SERVICE_ACCOUNT"])
        credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPE)
        client = gspread.authorize(credentials)
        st.session_state["spreadsheet"] = client.open(SHEET_NAME)
    return st.session_state["spreadsheet"]

@st.cache_data(ttl=300)
def cargar_dataframe(nombre_hoja):
    """
    Carga todos los datos de una hoja en Google Sheets como DataFrame.
    """
    try:
        sheet = get_fresh_spreadsheet().worksheet(nombre_hoja)
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"❌ Error al cargar hoja '{nombre_hoja}': {e}")
        return pd.DataFrame()

# === Conexión Inicial ===
try:
    spreadsheet = get_fresh_spreadsheet()
    with st.sidebar:
        with st.expander("🔧 Estado de conexión", expanded=False):
            st.success("✅ Conexión con Google Sheets exitosa")
            st.success(f"✅ Hoja activa: '{SHEET_NAME}'")
except Exception as e:
    st.sidebar.error("❌ Falló la conexión con Google Sheets")
    st.stop()

def calcular_leyes_sociales(sueldo_bruto, tipo_contrato):
    '''
    '''
    # Porcentajes leyes sociales
    TASAS = {
        "Indefinido": {
            "afp": 0.10,
            "salud": 0.07,
            "cesantia_trabajador": 0.006,
            "cesantia_empleador": 0.024,
            "sis": 0.0153,
            "atep": 0.0093
        },
        "Plazo Fijo": {
            "afp": 0.10,
            "salud": 0.07,
            "cesantia_trabajador": 0.0,
            "cesantia_empleador": 0.03,
            "sis": 0.0153,
            "atep": 0.0093
        },
        "Honorarios": {
            "afp": 0.0,
            "salud": 0.0,
            "cesantia_trabajador": 0.0,
            "cesantia_empleador": 0.0,
            "sis": 0.0,
            "atep": 0.0
        }
    }
    tasas = TASAS[tipo_contrato]
    detalle = {}

    for item, tasa in tasa.item():
        detalle[item] = round(sueldo_bruto * tasa)
    
    detalle["total_aportes"] = sum(detalle.values())
    
    return detalle
