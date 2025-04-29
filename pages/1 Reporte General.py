import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread
import json
import os

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
def cargar_lista(nombre_hoja, columna):
    """
    Carga los registros de una hoja específica y extrae los valores de una columna.

    Args:
        nombre_hoja (str): Nombre de la hoja en Google Sheets.
        columna (str): Nombre de la columna a extraer.

    Returns:
        list: Lista de valores únicos sin espacios vacíos.
    """
    try:
        sheet = get_fresh_spreadsheet().worksheet(nombre_hoja)
        data = sheet.get_all_records()
        return [r[columna] for r in data if r[columna].strip()]
    except:
        return []

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

# === Configuración Streamlit ===
# st.set_page_config(page_title="Dashboard de Reportes", layout="wide")
st.title("📊 Reporte General de Costos e Ingresos")

# === Cargar datos ===
try:
    costos_data = get_fresh_spreadsheet().worksheet("costos").get_all_records()
    ingresos_data = get_fresh_spreadsheet().worksheet("ingresos").get_all_records()
    df_costos = pd.DataFrame(costos_data)
    df_ingresos = pd.DataFrame(ingresos_data)
except Exception as e:
    st.error(f"❌ Error al cargar datos: {e}")
    st.stop()

# === Procesar fechas ===
for df, fecha_col in [(df_costos, "fecha_gasto"), (df_ingresos, "fecha_ingreso")]:
    if fecha_col in df.columns:
        df[fecha_col] = pd.to_datetime(df[fecha_col], format="%d/%m/%Y", errors="coerce")

# === Cálculos generales ===
total_costos = df_costos["valor_bruto"].sum()
total_ingresos = df_ingresos["valor_bruto"].sum()
balance = total_ingresos - total_costos

# === Tarjetas resumen ===
st.subheader("Resumen General")
col1, col2, col3 = st.columns(3)
col1.metric("\ud83d\udcb8 Total de Costos", f"${total_costos:,.0f}".replace(",", "."), help="Suma de todos los costos")
col2.metric("\ud83d\udcb0 Total de Ingresos", f"${total_ingresos:,.0f}".replace(",", "."), help="Suma de todos los ingresos")
col3.metric(
    "\ud83d\udcc8 Balance", 
    f"${balance:,.0f}".replace(",", "."),
    delta=f"{(balance / total_costos * 100):.2f}%" if total_costos > 0 else "",
    help="Ingresos - Costos"
)

st.divider()

# === Gráficos de distribución ===
st.subheader("Distribución de Costos por Ítem")
if not df_costos.empty and "item" in df_costos.columns:
    costos_por_item = df_costos.groupby("item")["valor_bruto"].sum().sort_values(ascending=False)
    st.bar_chart(costos_por_item, color="#FF0000")

st.subheader("Distribución de Ingresos por Ítem")
if not df_ingresos.empty and "item" in df_ingresos.columns:
    ingresos_por_item = df_ingresos.groupby("item")["valor_bruto"].sum().sort_values(ascending=False)
    st.bar_chart(ingresos_por_item, color="#008000")

st.divider()

# === Últimos registros ===
st.subheader("Últimos Registros")
st.write("\ud83d\udd34 Últimos 5 costos registrados")
if not df_costos.empty:
    st.dataframe(df_costos.sort_values("id", ascending=False).head(5), use_container_width=True)

st.write("\ud83d\udfe9 Últimos 5 ingresos registrados")
if not df_ingresos.empty:
    st.dataframe(df_ingresos.sort_values("id", ascending=False).head(5), use_container_width=True)
