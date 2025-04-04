import streamlit as st
from datetime import datetime
import pytz

st.title("Formulario de Registro de Ingresos")

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



# Inputs
st.divider()
st.subheader("Infromación General")

descripcion = st.text_input("Descripción del Ingreso")
valor_bruto = st.number_input("Valor Bruto del Ingreso", min_value=0, step=1, format="%d")
valor_neto  = valor_bruto * 0.19
iva = valor_bruto - valor_neto


# item
st.divider()
st.subheader("Tipo de Ingreso")

try:
    # Obtener lista dinámica de items desde la hoja 'items'
    items_sheet = spreadsheet.worksheet("items")
    data = items_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
    item_list = [row["item"] for row in data if row["item"].strip()]
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
        st.success("✅ Ingreso guardado con éxito")