import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import os

# Configuración de autenticación con Google Sheets usando google-auth
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Autenticación y conexión con Google Sheets
try:
    # Leer las credenciales desde secrets (Streamlit Cloud)
    service_account_info = json.loads(os.environ["GCP_SERVICE_ACCOUNT"])
    credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPE)
    client = gspread.authorize(credentials)
    st.write("✅ Conexión autenticada exitosamente con Google Sheets") # TODO: QUE EL DISPLAY DE ALERTAS DURE UN POCO EN PANTALLA
except Exception as e:
    st.error(f"❌ Error en la autenticación con Google Sheets: {e}")

# Intentar abrir la hoja de Google Sheets
SHEET_NAME = "prueba_streamlit"
try:
    # sheet = client.open(SHEET_NAME).sheet1
    spreadsheet = client.open(SHEET_NAME)
    sheet = spreadsheet.get_worksheet(0) # Abre la primera hoja por índice en vez de por nombre
    st.write(f"✅ Hoja de Google Sheets '{SHEET_NAME}' abierta exitosamente")
except Exception as e:
    st.error(f"❌ Error al abrir la hoja de Google Sheets: {e}")

# Estructura del Formulario
st.title("Formulario de Registro de Costos")

# Descripción Gasto
descripcion = st.text_input("Descripción del Gasto", placeholder='Descripción breve del gasto. Ej: "Pago Iva y 20% restante", "Compra Touchdown IQ 500 20 L".')

# Monto del Gasto
monto = st.number_input("Monto del Gasto", min_value=0.0, format="%.2f", step=int)

# Item/Cultivo/Centro de costos del gasto
    # Agregar opción para customizar lista de ítems
item = st.selectbox("Ítem", ['Aseo y Ornato', 'Campo General', 'Choclo', 'Frambuesas', 'Papas', 'Pasto', 'Peonías'], index=None, placeholder="Seleccione ítem o centro de costos del gasto")

# Proveedor de la compra/costo/gasto
    # Agregar opción para customizar lista de proveedores
proveedores = st.selectbox("Proveedor", [], index=None, placeholder="Seleccione proveedor") 

# N° folio boleta/factura

# Fecha del Gasto
    # Fecha en la que se efectuó el gasto/compra/costo

# Fecha de Emisión
    # Fecha de emisión de la boleta o factura

# Fecha de Vencimiento

if st.button("Guardar Registro"):
    try:
        # Intentar guardar los datos en la hoja
        sheet.append_row([descripcion, monto, item])
        st.success("¡Registro guardado con éxito!")
    except Exception as e:
        st.error(f"❌ Error al guardar el registro en Google Sheets: {e}")
