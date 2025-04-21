import streamlit as st
from datetime import datetime
from google.oauth2.service_account import Credentials
import gspread
import json
import os
import pytz

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

st.title("📋 Formulario de Registro de Ingresos")

spreadsheet = st.session_state.get("spreadsheet")
if not spreadsheet:
    st.error("❌ No se pudo acceder al documento. Verifica la conexión en la página principal.")
    st.stop()

# Obtener la hoja de ingresos
try:
    ingresos_sheet = spreadsheet.worksheet("ingresos")
except Exception as e:
    st.error(f"❌ No se pudo abrir la hoja 'ingresos': {e}")
    st.stop()

# ✅ Mostrar mensaje de éxito si se acaba de guardar un registro
if st.session_state.get("registro_guardado"):
    st.toast("Registro guardado con éxito", icon="✅")
    st.session_state["registro_guardado"] = False


# Inputs
st.divider()
st.subheader("Infromación General")

descripcion = st.text_input("Descripción del Ingreso")
valor_bruto = st.number_input("Valor Bruto del Ingreso", min_value=0, step=1, format="%d")
valor_neto  = valor_bruto * 0.19
iva = valor_bruto - valor_neto

# Formateo visual con separador de miles (solo display opcional)
monto_formateado = f"{valor_bruto:,}".replace(",", ".")  # convierte 10000 → "10.000"
st.write(f"Monto ingresado: ${monto_formateado}")

# item
st.divider()
st.subheader("Tipo de Ingreso")

try:
    # Obtener lista dinámica de items desde la hoja 'items'
    items_sheet = spreadsheet.worksheet("items")
    data = items_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
    item_list = [
        row["item"]
        for row in data
        if row["item"].strip() and row["item"] not in ["Aseo y Ornato"]
    ]
except Exception as e:
    st.error(f"❌ Error al cargar la lista de items: {e}")
    item_list = []

item = st.selectbox(
    "Ítem", 
    item_list,
    index=None, 
    placeholder="Seleccione ítem o centro de costos")

# Clientes
st.divider()
st.subheader("Clientes")

try:
    # Obtener lista dinámica de Clientes desde la hoja 'clientes'
    clientes_sheet = spreadsheet.worksheet("clientes")
    data = clientes_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
    clientes_list = [row["cliente"] for row in data if row["cliente"].strip()]
except Exception as e:
    st.error(f"❌ Error al cargar la lista de clientes: {e}")
    clientes_list = []

cliente_seleccionado = st.selectbox(
    "clientes", 
    clientes_list, 
    index=None, 
    placeholder="Seleccione cliente"
)

st.divider()
st.subheader("Fecha del Ingreso")

fecha_ingreso = st.date_input("Fecha del Ingreso")

st.divider()
comentario = st.text_area("Comentario (opcional)", placeholder="Notas adicionales")

# Botón de guardar registro

if st.button("Guardar Registro"):
    if not descripcion.strip():
        st.warning("La descripción es obligatoria.")
    elif valor_bruto <= 0:
        st.warning("El valor bruto debe ser mayor a 0.")
    # Agregar más a medida que aumenten las columnas/campos.
    else:
        try:
            headers = ingresos_sheet.row_values(1)
            zona_horaria = pytz.timezone('Chile/Continental')
            fecha_envio = datetime.now(zona_horaria).strftime("%d/%m/%Y %H:%M:%S")
            nuevo_id = len(ingresos_sheet.get_all_values())

            registro = {
                "id": nuevo_id,
                "fecha_envio": fecha_envio,
                "descripcion": descripcion,
                "valor_bruto": valor_bruto,
                "valor_neto" : valor_neto,
                "iva" : iva,
                "item" : item,
                "cliente" : cliente_seleccionado,
                "fecha_ingreso": fecha_ingreso.strftime("%d/%m/%Y"),
                "comentarios": comentario
            }

            fila_final = [registro.get(col, "") for col in headers]
            ingresos_sheet.append_row(fila_final)
            
            # ✅ Marcar éxito y refrescar
            st.session_state["registro_guardado"] = True  # Marcar que se guardó con éxito
            
            # 🔄 Refrescar la app
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error al guardar el registro en Google Sheets: {e}")
            st.session_state["registro_guardado"] = False  # Resetear si falló