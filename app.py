import gspread
from google.oauth2.service_account import Credentials
import json
import os
import streamlit as st


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
    st.write("✅ Conexión autenticada exitosamente con Google Sheets")
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

# Título del Formulario
st.title("Formulario de Registro de Costos")

# Descripción Gasto
descripcion = st.text_input(
    "Descripción del Gasto", 
    placeholder='Descripción breve del gasto. Ej: "Pago Iva y 20% restante", "Compra Touchdown IQ 500 20 L".')

# Monto del Gasto - solo enteros con separador de miles
monto = st.number_input(
    "Monto del Gasto/Compra", 
    min_value=0, 
    step=1,
    format="%d"
)

# Formateo visual con separador de miles (solo display opcional)
monto_formateado = f"{monto:,}".replace(",", ".")  # convierte 10000 → "10.000"

st.write(f"Monto ingresado: ${monto_formateado}")

# Item/Cultivo/Centro de costos del gasto
    # Agregar opción para customizar lista de ítems
item = st.selectbox(
    "Ítem", 
    ['Aseo y Ornato', 'Campo General', 'Choclo', 'Frambuesas', 'Papas', 'Pasto', 'Peonías'], 
    index=None, 
    placeholder="Seleccione ítem o centro de costos del gasto")

# Proveedor de la compra/costo/gasto
    # TODO: Agregar opción para customizar lista de proveedores (HECHO)

# Obtener lista dinámica de proveedores desde la hoja 'proveedores'
try:
    proveedores_sheet = spreadsheet.worksheet("proveedores")
    data = proveedores_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
    proveedores_list = [row["proveedores"] for row in data if row["proveedores"].strip()]
except Exception as e:
    st.error(f"❌ Error al cargar la lista de proveedores: {e}")
    proveedores_list = []

proveedor_seleccionado = st.selectbox(
    "Proveedor", 
    proveedores_list, 
    index=None, 
    placeholder="Seleccione proveedor") 

# Input de nuevo proveedor
nuevo_proveedor = st.text_input(
    "¿Proveedor no está en la lista? Escriba nuevo proveedor. De lo contrario dejar sección en blanco",
    placeholder="Nombre del nuevo proveedor")

# Decidir qué valor usar
proveedor_final = nuevo_proveedor.strip() if nuevo_proveedor else proveedor_seleccionado

# Agrega nuevo proveedor a la lista
if nuevo_proveedor and nuevo_proveedor.strip() not in proveedores_list:
    proveedores_sheet.append_row(["", nuevo_proveedor.strip()])       # ⚠️ El primer valor "" es para dejar la columna index vacía, en caso de querer llenarla luego manualmente o con otra función.

# TODO: Generar indices ("Id") en cada hoja del google sheet

# N° Folio boleta/factura
numero_folio = st.number_input(
    "Número de Folio de Boleta/Factura",
    min_value=None,
    step=1,
    format="%d",
    placeholder="N° de boleta o factura"
)

# Fecha del Gasto
    # Fecha en la que se efectuó el gasto/compra/costo
fecha_gasto = st.date_input(
    "Fecha del Gasto o Compra",
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
    # Primero validamos que los campos Descripción Gasto, Monto del Gasto, Ítem y Proveedor no estén vacíos
    errores = []

    if not descripcion.strip():
        errores.append("La descripción del gasto es obligatoria.")
    if monto == 0:
        errores.append("El monto debe ser mayor que cero.")
    if not item:
        errores.append("Debe seleccionar un ítem.")
    if not proveedor_final:
        errores.append("Debe seleccionar o ingresar un proveedor.")

    if errores:
        for err in errores:
            st.warning(err)
    else:
        # Si todo está en orden se procede a agregar los datos a la planilla
        try:
            sheet.append_row([
                descripcion,
                monto,
                item,
                proveedor_final,
                numero_folio,
                fecha_gasto,
                fecha_emision,
                fecha_vencimiento
            ])
            st.success("¡Registro guardado con éxito!")
        except Exception as e:
            st.error(f"❌ Error al guardar el registro en Google Sheets: {e}")
