from google.oauth2.service_account import Credentials
import gspread
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import pandas as pd
import streamlit as st

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
def cargar_dataframe(nombre_hoja):
    """
    Carga todos los datos de una hoja en Google Sheets como DataFrame.
    """
    try:
        sheet = get_fresh_spreadsheet().worksheet(nombre_hoja)
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"❌ Error al cargar hoja '{nombre_hoja}': {e}")
        return pd.DataFrame()

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
    dataframes_dict = {
        "rrhh": cargar_dataframe("rrhh"),
        "agroquimicos": cargar_dataframe("agroquimicos"),
        "maquinaria": cargar_dataframe("maquinaria"),
        "administracion": cargar_dataframe("administracion"),
        "seguros": cargar_dataframe("seguros"),
        "inversiones": cargar_dataframe("inversiones"),
        "servicios_externos": cargar_dataframe("servicios_externos"),
        "servicios_basicos": cargar_dataframe("servicios_basicos"),
        "combustibles": cargar_dataframe("combustibles"),
        "gastos_varios": cargar_dataframe("gastos_varios"),
        "ingresos": cargar_dataframe("ingresos"),
    }
except Exception as e:
    st.error(f"❌ Error al cargar datos: {e}")
    st.stop()

# === Procesar tipos fechas ===

columnas_fechas = ["fecha_ingreso", "fecha_vencimiento_30", "fecha_vencimiento_60", "fecha_vencimiento_90", "fecha_vencimiento_120"]

columnas_fecha_hora = ["fecha_envio"]

# Procesar columnas con fecha y hora
for nombre, df in dataframes_dict.items():
    for col in columnas_fecha_hora:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%d/%m/%Y %H:%M:%S", errors="coerce")


# Procesar columnas solo con fecha
for nombre, df in dataframes_dict.items():
    for col in columnas_fechas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%d/%m/%Y", errors="coerce" )

# OJO CON LA DIVISIÓN DE TEMPORADAS:
    # T2223
    # T2324
    # T2425 

# === Cálculos generales ===
    
    # NOTA : rrhh cambiará

total_costos = sum(df["valor_bruto"].sum() for df in dataframes_dict.values())
total_ingresos = dataframes_dict["ingresos"]["valor_bruto"].sum()
balance = total_ingresos - total_costos

# === Tarjetas resumen ===
st.subheader("Resumen General")
col1, col2, col3 = st.columns(3)
col1.metric("💸 Total de Costos", f"${total_costos:,.0f}".replace(",", "."), help="Suma de todos los costos")
col2.metric("💰 Total de Ingresos", f"${total_ingresos:,.0f}".replace(",", "."), help="Suma de todos los ingresos")
col3.metric(
    "📈 Balance", 
    f"${balance:,.0f}".replace(",", "."),
    delta=f"{(balance / total_costos * 100):.2f}%" if total_costos > 0 else "",
    help="Ingresos - Costos"
)

st.divider()

# === Gráficos de distribución ===

df_costos_total = pd.concat(
    [df for nombre, df in dataframes_dict.items() if nombre != "ingresos" and not df.empty],
    ignore_index=True
)

# Agrupar por centro de costos
costos_por_ceco = df_costos_total.groupby("centro_costo")["valor_bruto"].sum().sort_values(ascending=False)

# Gráfico de Barras con Matplotlib

fig, ax = plt.subplots(figsize=(10, 5))
costos_por_ceco.plot(kind="bar", color="#FF0000", ax=ax)

# Etíquetas y título

ax.set_title("Distribución de Costos por Centro de Costos", fontsize=16)
# ax.set_xlabel("Centro de Costos")
ax.set_ylabel("Costo Total")
ax.tick_params(axis="x", rotation=45)

# Fondo transparente

fig.patch.set_alpha(0.0)   # Fondo de la figura
ax.patch.set_alpha(0.0)    # Fondo del área de gráficos

# Display de valores en eje "y" en formato 1.2 M
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x / 1e6:.1f} M"))

# Mostrar en Streamlit
st.pyplot(fig)

# st.subheader("Distribución de Costos por Centro de Costos")
# st.bar_chart(costos_por_ceco, color="#FF0000")

# for nombre, df in dataframes_dict.items():
#     if not df.empty and nombre != "ingresos":
#         costos_por_ceco = df.groupby("centro_costo")["valor_bruto"].sum().sort_values(ascending=False)
#         st.bar_chart(costos_por_ceco, color="#FF0000")

# INGRESOS POR CULTIVO (?)

# st.subheader("Distribución de Ingresos por Ítem")
# if not df_ingresos.empty and "item" in df_ingresos.columns:
#     ingresos_por_item = df_ingresos.groupby("item")["valor_bruto"].sum().sort_values(ascending=False)
#     st.bar_chart(ingresos_por_item, color="#008000")

# st.divider()

# # === Últimos registros ===
# st.subheader("Últimos Registros")
# st.write("\ud83d\udd34 Últimos 5 costos registrados")
# if not df_costos.empty:
#     st.dataframe(df_costos.sort_values("id", ascending=False).head(5), use_container_width=True)

# st.write("\ud83d\udfe9 Últimos 5 ingresos registrados")
# if not df_ingresos.empty:
#     st.dataframe(df_ingresos.sort_values("id", ascending=False).head(5), use_container_width=True)
