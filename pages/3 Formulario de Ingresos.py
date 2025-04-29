import streamlit as st
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
import gspread
import json
import os
import pytz

# Configuración de autenticación con Google Sheets
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_NAME = "prueba_streamlit"  # ⚠️Modificar en producción⚠️

def get_fresh_spreadsheet():
    """
    Crea y retorna una conexión reutilizable al documento de Google Sheets.

    Reutiliza una conexión existente guardada en st.session_state si está disponible,
    y la renueva si no existe.

    Returns:
        gspread.Spreadsheet: Objeto Spreadsheet conectado y listo para usar.
    """
    if "spreadsheet" not in st.session_state:
        service_account_info = json.loads(os.environ["GCP_SERVICE_ACCOUNT"])
        credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPE)
        client = gspread.authorize(credentials)
        st.session_state["spreadsheet"] = client.open(SHEET_NAME)
    return st.session_state["spreadsheet"]

@st.cache_data(ttl=300)
def cargar_lista(nombre_hoja, columna):
    """
    Carga los registros de una hoja específica y extrae los valores de una columna.

    Args:
        nombre_hoja (str): Nombre de la hoja en el documento de Google Sheets.
        columna (str): Nombre de la columna a extraer.

    Returns:
        list: Lista de valores únicos, sin espacios vacíos.
    """
    try:
        sheet = get_fresh_spreadsheet().worksheet(nombre_hoja)
        data = sheet.get_all_records()
        return [r[columna] for r in data if r[columna].strip()]
    except:
        return []

# Intentar conexión
try:
    spreadsheet = get_fresh_spreadsheet()
    with st.sidebar:
        with st.expander("🔧 Estado de conexión", expanded=False):
            st.success("✅ Conexión con Google Sheets exitosa")
            st.success(f"✅ Hoja activa: '{SHEET_NAME}'")
except Exception as e:
    st.sidebar.error("❌ Falló la conexión con Google Sheets")
    st.stop()

st.title("📋 Formulario de Registro de Ingresos")

# ✅ Mostrar mensaje de éxito si se acaba de guardar un registro
if st.session_state.get("registro_guardado"):
    st.toast("Registro guardado con éxito", icon="✅")
    st.session_state["registro_guardado"] = False

# Inputs
st.subheader("Información General")

descripcion = st.text_input("Descripción del Ingreso")
valor_bruto = st.number_input("Valor Bruto del Ingreso", min_value=0, step=1, format="%d")
iva = int(valor_bruto * 0.19)
valor_neto = valor_bruto - iva
monto_formateado = f"{valor_bruto:,}".replace(",", ".")
st.write(f"Monto ingresado: ${monto_formateado}")

# Cultivo
st.divider()
st.subheader("Cultivo")
cultivo_list = cargar_lista("cultivos", "cultivo")
cultivo = st.selectbox("Seleccione cultivo o centro de costos", cultivo_list, index=None, placeholder="Cultivo")

# Clientes
st.divider()
st.subheader("Clientes")
clientes_list = cargar_lista("clientes", "cliente")
cliente = st.selectbox("Seleccione cliente", clientes_list, index=None, placeholder="Cliente")

# Folio y Fecha
st.divider()
st.subheader("Fecha del Ingreso")
numero_folio = st.text_input("Número de Folio", placeholder="Dejar en blanco si no aplica").strip() or "N/A"
fecha_ingreso = st.date_input("Fecha del Ingreso", value=datetime.today().date(), format="DD/MM/YYYY")

# Vencimientos
st.divider()
st.subheader("Vencimientos")

def fecha_vencimiento_input(dias):
    opciones = ["Establecer fecha", "No aplica", "Por definir"]
    eleccion = st.radio(f"**Vencimiento a {dias} días:**", opciones, key=f"radio_venc_{dias}")
    if eleccion == "Establecer fecha":
        sugerida = datetime.today() + timedelta(days=dias)
        fecha = st.date_input(f"Elija la fecha para {dias} días", value=sugerida, key=f"fecha_venc_{dias}", format="DD/MM/YYYY")
        return fecha.strftime("%d/%m/%Y")
    elif eleccion == "Por definir":
        return "Por definir"
    return "N/A"

def pago_input(vencimiento, dias):
    bancos_lista = cargar_lista("tipo_pagos", "tipo_pago")
    if vencimiento == "Por definir":
        return "Por definir"
    elif vencimiento == "N/A":
        return "N/A"
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

# Guardar
if st.button("Guardar Registro"):
    errores = []
    if not descripcion.strip(): errores.append("La descripción es obligatoria.")
    if valor_bruto <= 0: errores.append("El valor bruto debe ser mayor que cero.")
    if not cultivo: errores.append("Debe seleccionar un cultivo.")
    if not cliente: errores.append("Debe seleccionar un cliente.")

    if errores:
        for err in errores: st.warning(err)
    else:
        try:
            sheet = spreadsheet.worksheet("ingresos")
            headers = sheet.row_values(1)
            fecha_envio = datetime.now(pytz.timezone('Chile/Continental')).strftime("%d/%m/%Y %H:%M:%S")
            nuevo_id = len(sheet.get_all_values())

            registro = {
                "id": nuevo_id,
                "fecha_envio": fecha_envio,
                "descripcion": descripcion,
                "valor_bruto": valor_bruto,
                "valor_neto": valor_neto,
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
            sheet.append_row(fila_final)
            st.session_state["registro_guardado"] = True
            st.toast("Registro guardado con éxito", icon="✅")
            # st.rerun()
            # 🔄 Recarga la página
                # Nota: Hay otras formas de recargar la página pero hasta el momento
                #       Este fue el que mejor funcionó.
            st.markdown("""
                <meta http-equiv="refresh" content="0">
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Error al guardar el registro en Google Sheets: {e}")
