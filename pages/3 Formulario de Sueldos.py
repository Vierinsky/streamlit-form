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

# === Calculo leyes sociales ===

# Porcentajes leyes sociales
    # REVISAR
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

def calcular_leyes_sociales(sueldo_bruto: int, tipo_contrato: str) -> dict:
    """
    Calcula el desglose de leyes sociales para un trabajador en Chile según su tipo de contrato.

    Args:
        sueldo_bruto (int): Sueldo bruto mensual del trabajador.
        tipo_contrato (str): Tipo de contrato del trabajador. Debe ser una clave válida en el diccionario TASAS.

    Returns:
        dict: Un diccionario con el monto correspondiente a cada componente de las leyes sociales, 
              según las tasas establecidas para el tipo de contrato. Si el tipo de contrato no existe 
              en TASAS, se retorna un diccionario vacío.
    
    Ejemplo de retorno:
        {
            "afp": 10000,
            "salud": 7000,
            "seguro_cesantia": 3000
        }
    """
    tasas = TASAS.get(tipo_contrato	, {})
    detalle = {}

    for item, tasa in tasas.item():
        detalle[item] = round(sueldo_bruto * tasa)
    
    detalle["total_aportes"] = sum(detalle.values())
    
    return detalle

# === Formulario Principal ===
st.title("📋 Formulario de Registro de Sueldos")

st.text_input(
    "Escriba nombre del trabajador",
    placeholder="Nombre completo"
)

tipo_contrato = st.radio("Seleccione tipo de contrato", ["Indefinido", "Plazo Fijo", "Honorarios"])

sueldo_bruto = st.number_input(
    "Inserte sueldo bruto:",
    min_value=0, 
    step=1,
    format="%d"
)

leyes = calcular_leyes_sociales(sueldo_bruto, tipo_contrato)

# Formateo visual con separador de miles (solo display opcional)
monto_formateado = f"{sueldo_bruto:,}".replace(",", ".")  # convierte 10000 → "10.000"
st.write(f"Sueldo Bruto = ${monto_formateado}")
st.write(f"Prevision (AFP) = ${leyes['afp']}")
st.write(f"Salud (Fonasa o Isapre) = ${leyes['salud']}")
st.write(f"Seguro de Cesantía (Trabajador) = ${leyes['cesantia_trabajador']}")
st.write(f"Seguro de Cesantía (Empleador) = ${leyes['cesantia_empleador']}")
st.write(f"Cotización SIS (por invalidez y sobrevivencia) = ${leyes['sis']}")
st.write(f"Accidentes del Trabajo (ATEP) = ${leyes['atep']}")

 
# 1. Ingrese sueldo bruto
#       - Que muestre desglose.
#       - Que permita dividir el sueldo según días trabajados en x cultivo.
#       - Que se agregue nombre del trabajador. 

# 2. Desea agregar Gratificaciones?

# Nota: 
#   ¿Debe haber sección banco también?
#   ¿Si se tiene a un trabajador contratado se debe auto agregar todos los meses su sueldo?
#   ¿Se necesita info más detallada del trabajador? Ej: RUT u otros.

# 3. Mostrar resúmen
# 4. Sección "Comentario"
# 4. Enviar formulario