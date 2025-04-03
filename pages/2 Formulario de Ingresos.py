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
descripcion = st.text_input("Descripción del Ingreso")
monto = st.number_input("Monto del Ingreso", min_value=0, step=1, format="%d")
fecha_ingreso = st.date_input("Fecha del Ingreso")
comentario = st.text_area("Comentario (opcional)", placeholder="Notas adicionales")

if st.button("Guardar Ingreso"):
    if not descripcion.strip():
        st.warning("La descripción es obligatoria.")
    elif monto <= 0:
        st.warning("El monto debe ser mayor a 0.")
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
            "monto": monto,
            "fecha_ingreso": fecha_ingreso.strftime("%d/%m/%Y"),
            "comentarios": comentario
        }

        fila_final = [registro.get(col, "") for col in headers]
        ingresos_sheet.append_row(fila_final)
        st.success("✅ Ingreso guardado con éxito")