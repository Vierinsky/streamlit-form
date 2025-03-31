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
descripcion = st.text_input(
    "Descripción del Gasto", 
    placeholder='Descripción breve del gasto. Ej: "Pago Iva y 20% restante", "Compra Touchdown IQ 500 20 L".')

# Monto del Gasto
monto = st.number_input(
    "Monto del Gasto/Compra", 
    min_value=0.0, 
    format="%.2f", 
    step=1.0)

# Item/Cultivo/Centro de costos del gasto
    # Agregar opción para customizar lista de ítems
item = st.selectbox(
    "Ítem", 
    ['Aseo y Ornato', 'Campo General', 'Choclo', 'Frambuesas', 'Papas', 'Pasto', 'Peonías'], 
    index=None, 
    placeholder="Seleccione ítem o centro de costos del gasto")

# Proveedor de la compra/costo/gasto
    # TODO: Agregar opción para customizar lista de proveedores
proveedores_list = ["Agricola Alta Gracia Ltda", "Agricola innova", "Agencia Aduana J Sanhueza", "Agrotrust", "Andrea Reyes", "Austral Innova", "Cals", "Carlos Levin", "Chilemat Pagado a Innova", "Coagra", "Colun (Jaime Vergara)", "Copeval", "Covepa", "CyC Empresas SpA", "Dick Houter", "Dripco", "Entre Riegos del Sur", "Estuario", "Ferosor", "Green Works E 123.650", "Hernan Muñoz", "Lilian Franco", "Luis Vera", "Marcelo Gatica", "Martinez y Valdivieso","Matias Castillo", "Pablo Reyes", "Rodolfo Castillo", "Roxana del Carmen T", "Serv Mant Vergara", "Telemetry", "Tomás Schmidt"]

proveedores = st.selectbox(
    "Proveedor", 
    proveedores_list, 
    index=None, 
    placeholder="Seleccione proveedor") 

# N° Folio boleta/factura
numero_folio = st.number_input(
    "Número de Folio",
    min_value=None,
    step=1,
    format="%d",
    placeholder="N° de boleta o factura"
)

# Fecha del Gasto
    # Fecha en la que se efectuó el gasto/compra/costo
fecha_gasto = st.date_input(
    "Fecha del Gasto",
    value="today",
    format="DD/MM/YYYY"
)

# Fecha de Emisión
    # Fecha de emisión de la boleta o factura
fecha_emision = st.date_input(
    "Fecha de Emisión Boleta/Factura",
    value="today",
    format="DD/MM/YYYY"
)

# Fecha de Vencimiento
fecha_vencimiento = st.date_input(
    "Fecha de Vencimiento Boleta/Factura",
    value="today",
    format="DD/MM/YYYY"
)

if st.button("Guardar Registro"):
    try:
        # Intentar guardar los datos en la hoja
        sheet.append_row([descripcion, monto, item, proveedores, numero_folio, fecha_gasto, fecha_emision, fecha_vencimiento])
        st.success("¡Registro guardado con éxito!")
    except Exception as e:
        st.error(f"❌ Error al guardar el registro en Google Sheets: {e}")
