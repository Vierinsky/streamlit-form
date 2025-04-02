from datetime import datetime
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

# Intentar abrir la hoja de Google Sheets
SHEET_NAME = "prueba_streamlit"             # ⚠️Modificar en producción⚠️

# Autenticación y conexión con Google Sheets
try:
    service_account_info = json.loads(os.environ["GCP_SERVICE_ACCOUNT"])             # ⚠️Modificar en producción⚠️
    credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPE)
    client = gspread.authorize(credentials)

    spreadsheet = client.open(SHEET_NAME)
    sheet = spreadsheet.worksheet("costos")

    # ✅ Mostrar estado en expander discreto
    with st.expander("🔧 Estado de conexión (click para ver)", expanded=False):
        st.success("✅ Conexión autenticada exitosamente con Google Sheets")
        st.success(f"✅ Hoja de Google Sheets '{SHEET_NAME}' abierta exitosamente")

except Exception as e:
    st.error(f"❌ Error de conexión con Google Sheets: {e}")


# Título del Formulario
st.title("Formulario de Registro de Costos")

# Descripción Gasto
descripcion = st.text_input(
    "Descripción del Gasto", 
    placeholder='Descripción breve del gasto. Ej: "Pago Iva y 20% restante", "Compra Touchdown IQ 500 20 L".')

# Valor bruto del Gasto - solo valores tipo int
valor_bruto = st.number_input(
    "Valor Bruto del Gasto/Compra (IVA incluido)", 
    min_value=0, 
    step=1,
    format="%d"
)

iva = valor_bruto * 0.19
valor_neto = valor_bruto - iva

# Formateo visual con separador de miles (solo display opcional)
monto_formateado = f"{valor_bruto:,}".replace(",", ".")  # convierte 10000 → "10.000"

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
    placeholder="Seleccione proveedor"
) 

# Limpiar campo de texto si se seleccionó uno de la lista
if proveedor_seleccionado and st.session_state.get("nuevo_proveedor"):
    st.session_state["nuevo_proveedor"] = ""

# Input de nuevo proveedor
nuevo_proveedor = st.text_input(
    "¿Proveedor no está en la lista? Escriba nuevo proveedor. De lo contrario dejar en blanco",
    placeholder="Nombre del nuevo proveedor",
    key="nuevo_proveedor"
)

# Decidir qué valor usar
proveedor_final = nuevo_proveedor.strip() if nuevo_proveedor else proveedor_seleccionado

# Agrega nuevo proveedor a la lista y le genera un id
if not proveedor_seleccionado and nuevo_proveedor.strip() and nuevo_proveedor.strip() not in proveedores_list:
    num_filas_proveedores = len(proveedores_sheet.get_all_values())
    nuevo_id_proveedor = num_filas_proveedores  # Asumiendo que fila 1 es encabezado
    proveedores_sheet.append_row([nuevo_id_proveedor, nuevo_proveedor.strip()])

# TODO: Generar indices ("Id") en cada hoja del google sheet

# Priorizar proveedor seleccionado
proveedor_final = proveedor_seleccionado if proveedor_seleccionado else nuevo_proveedor.strip()

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

# Comentario opcional del usuario
comentario = st.text_area(
    "Comentario (opcional)", 
    placeholder="Agregue una nota o comentario sobre este gasto"
)

# Botón de guardar registro
if st.button("Guardar Registro"):
    # Primero validamos que los campos Descripción Gasto, Valor Bruto del Gasto, Ítem y Proveedor no estén vacíos
    errores = []

    if not descripcion.strip():
        errores.append("La descripción del gasto es obligatoria.")
    if valor_bruto == 0:
        errores.append("El valor bruto debe ser mayor que cero.")
    if not item:
        errores.append("Debe seleccionar un ítem.")
    if not proveedor_final:
        errores.append("Debe seleccionar o ingresar un proveedor.")
    if numero_folio < 0:
        errores.append("N° de folio debe ser un número positivo")

    if errores:
        for err in errores:
            st.warning(err)
    else:
        # Si todo está en orden se procede a agregar los datos a la planilla
        try:
            # Obtener los encabezados (primera fila de la hoja)
            headers = sheet.row_values(1)

            # Registra la hora actual (hora de envio del formulario)
            fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")    # datetime se transforma a string

            # Obtener el nuevo índice (número de fila - 1 para no contar el encabezado)
            num_filas_existentes = len(sheet.get_all_values())
            nuevo_index = num_filas_existentes  # Si hay encabezado, el índice empieza desde 1

            # Armar diccionario con los datos usando los nombres de las columnas
            registro = {
                "id" : nuevo_index,
                "fecha_envio": fecha_hora_actual,
                "descripcion": descripcion,
                "valor_bruto": valor_bruto,
                "valor_neto": valor_neto,
                "iva": iva,
                "item": item,
                "proveedor": proveedor_final,
                "numero_folio": numero_folio,
                "fecha_gasto": fecha_gasto.strftime("%d/%m/%Y"),                # datetime se transforma a string
                "fecha_emision": fecha_emision.strftime("%d/%m/%Y"),            # datetime se transforma a string
                "fecha_vencimiento": fecha_vencimiento.strftime("%d/%m/%Y"),    # datetime se transforma a string
                "comentarios": comentario
            }

            # Crear la fila final según el orden real de los encabezados
            fila_final = [registro.get(col, "") for col in headers]

            # Insertar la fila
            sheet.append_row(fila_final)
            st.success("¡Registro guardado con éxito!")

            # Solo si se usó un nuevo proveedor y no está en la lista
            if not proveedor_seleccionado and nuevo_proveedor.strip() and nuevo_proveedor.strip() not in proveedores_list:
                proveedores_sheet.append_row(["", nuevo_proveedor.strip()])

        except Exception as e:
            st.error(f"❌ Error al guardar el registro en Google Sheets: {e}")
