import streamlit as st
from datetime import datetime, timedelta
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
    st.error("❌ No se pudo acceder al documento. Verifica la conexión")
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
# st.divider()
st.subheader("Infromación General")

descripcion = st.text_input("Descripción del Ingreso")
valor_bruto = st.number_input("Valor Bruto del Ingreso", min_value=0, step=1, format="%d")
iva = int(valor_bruto * 0.19)       # Redondea hacia abajo
valor_neto = valor_bruto - iva

# Formateo visual con separador de miles (solo display opcional)
monto_formateado = f"{valor_bruto:,}".replace(",", ".")  # convierte 10000 → "10.000"
st.write(f"Monto ingresado: ${monto_formateado}")

# Cultivo
st.divider()
st.subheader("Cultivo")

try:
    # Obtener lista dinámica de cultivos desde la hoja 'cultivos'
    items_sheet = spreadsheet.worksheet("cultivos")
    data = items_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
    cultivo_list = [r["cultivo"] for r in data if r["cultivo"].strip()]
    
except Exception as e:
    st.error(f"❌ Error al cargar la lista de cultivos: {e}")
    cultivo_list = []

cultivo = st.selectbox(
    "Seleccione cultivo o centro de costos", 
    cultivo_list,
    index=None, 
    placeholder="Cultivo")

# Clientes
st.divider()
st.subheader("Clientes")

try:
    # Obtener lista dinámica de Clientes desde la hoja 'clientes'
    clientes_sheet = spreadsheet.worksheet("clientes")
    data = clientes_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
    clientes_list = [r["cliente"] for r in data if r["cliente"].strip()]
except Exception as e:
    st.error(f"❌ Error al cargar la lista de clientes: {e}")
    clientes_list = []

cliente = st.selectbox(
    "Seleccione cliente", 
    clientes_list, 
    index=None, 
    placeholder="Cliente"
)

# Folio y Fecha
st.divider()
st.subheader("Fecha del Ingreso")


numero_folio = st.text_input("Número de Folio", placeholder="Dejar en blanco si no aplica").strip() or "N/A"
fecha_ingreso = st.date_input("Fecha del Ingreso", format="DD/MM/YYYY")

# Vencimientos
st.divider()
st.subheader("Vencimientos")

def fecha_vencimiento_input(dias, fecha_ingreso):
    """
    Despliega un radio para elegir vencimiento a X días y muestra un date_input si aplica.

    Args:
        dias (int): Número de días del vencimiento (30, 60, 90, 120...).
        fecha_ingreso (datetime.date): Fecha base sobre la cual calcular el vencimiento sugerido.

    Returns:
        str: Fecha como string en formato "%d/%m/%Y", o "Por definir", o "N/A"
    """
    opciones = ["Establecer fecha", "No aplica", "Por definir"]
    eleccion = st.radio(f"**Vencimiento a {dias} días:**", opciones, key=f"radio_venc_{dias}")

    if eleccion == "Establecer fecha":
        # Fecha sugerida = fecha_ingreso + dias
        fecha_sugerida = fecha_ingreso + timedelta(days=dias)
        fecha = st.date_input(
            f"Elija la fecha para {dias} días",
            value=fecha_sugerida,
            key=f"fecha_venc_{dias}",
            format="DD/MM/YYYY"
        )
        return fecha.strftime("%d/%m/%Y")
    elif eleccion == "Por definir":
        return "Por definir"
    else:
        return "N/A"

def pago_input(vencimiento, dias):
    data = spreadsheet.worksheet("tipo_pagos").get_all_records()
    bancos_lista = [r["tipo_pago"] for r in data if r["tipo_pago"].strip()]
    if vencimiento == "Por definir":
        return "Por definir"
    elif vencimiento == "N/A":
        return "N/A"
    else:
        return st.selectbox("Seleccione forma de pago", bancos_lista, index=None, placeholder="Forma de pago", key=f"pago_{dias}")

vencimiento_30 = fecha_vencimiento_input(30)
pago_30 = pago_input(vencimiento_30, 30)
vencimiento_60 = fecha_vencimiento_input(60)
pago_60 = pago_input(vencimiento_60, 60)
vencimiento_90 = fecha_vencimiento_input(90)
pago_90 = pago_input(vencimiento_90, 90)
vencimiento_120 = fecha_vencimiento_input(120)
pago_120 = pago_input(vencimiento_120, 120)

# Comentarios
st.divider()
comentario = st.text_area("Comentario (opcional)", placeholder="Notas adicionales")

# Botón de guardar registro
if st.button("Guardar Registro"):
    errores = []
    if not descripcion.strip():
        st.warning("La descripción es obligatoria.")
    if valor_bruto <= 0:
        errores.append("El valor bruto debe ser mayor que cero.")
    if not cultivo:
        errores.append("Debe seleccionar un cultivo.")
    if not cliente:
        errores.append("Debe seleccionar un cliente.")

    if errores:
        for err in errores:
            st.warning(err)
    else:
        try:
            ingresos_sheet = spreadsheet.worksheet("ingresos")
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
                "iva": iva,
                "cultivo": cultivo,
                "cliente": cliente,
                "numero_folio": numero_folio,
                "fecha_ingreso": fecha_ingreso.strftime("%d/%m/%Y"),
                "fecha_vencimiento_30": vencimiento_30,
                "tipo_pago_30": pago_30,
                "fecha_vencimiento_60": vencimiento_60,
                "tipo_pago_60": pago_60,
                "fecha_vencimiento_90": vencimiento_90,
                "tipo_pago_90": pago_90,
                "fecha_vencimiento_120": vencimiento_120,
                "tipo_pago_120": pago_120,
                "comentarios": comentario
            }

            fila_final = [registro.get(col, "") for col in headers]
            ingresos_sheet.append_row(fila_final)
            
            # ✅ Marcar éxito y refrescar

            st.session_state["registro_guardado"] = True
            st.toast("Registro guardado con éxito", icon="✅")
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error al guardar el registro en Google Sheets: {e}")