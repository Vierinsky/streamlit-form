from google.oauth2.service_account import Credentials
import gspread
import json
import matplotlib.pyplot as plt                 # Evaluar si se usará. Si no, para sacarlo. Sacar de requirements.txt
from matplotlib.ticker import FuncFormatter     # Evaluar si se usará. Si no, para sacarlo
import os
import pandas as pd
import plotly.graph_objects as go    # TESTING (para gráficos más interactivos)
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

# === Gráficos ===

df_costos_total = pd.concat(
    [df for nombre, df in dataframes_dict.items() if nombre != "ingresos" and not df.empty],
    ignore_index=True
)

# Agrupar por centro de costos (Sumatoria costos)
costos_por_ceco = df_costos_total.groupby("centro_costo")["valor_bruto"].sum().sort_values(ascending=False)

# === Gráfico de barras ===
# Gráfico de barras con pyplot (Más interactivo)

# Lista de colores (se puede expandir o generar dinámicamente)
colores = [
    "#e74c3c",  # Rojo intenso (Alizarin)
    "#3498db",  # Azul claro (Peter River)
    "#2ecc71",  # Verde brillante (Emerald)
    "#9b59b6",  # Púrpura medio (Amethyst)
    "#f1c40f",  # Amarillo dorado (Sun Flower)
    "#e67e22",  # Naranja quemado (Carrot)
    "#1abc9c",  # Verde agua (Turquoise)
    "#34495e",  # Azul gris oscuro (Wet Asphalt)
    "#95a5a6",  # Gris claro (Concrete)
    "#d35400"   # Naranja profundo (Pumpkin)
]

# centro_de_costos = [
#     "rrhh", "agroquimicos", "maquinaria", "administracion",
# "seguros", "inversiones", "servicios_externos",
# "servicios_basicos", "combustibles", "gastos_varios"
# ]

# Lista de valores reales que aparecen en la columna 'centro_costo'
centros_costo_valores = [
    "RRHH", "Agroquimicos", "Maquinaria", "Administracion",
    "Seguros", "Inversiones", "Servicio Externos MMOO",
    "Servicios Básicos", "Combustibles", "Gastos Varios / Otros"
]

# Mapeo fijo: centro de costo → color
ceco_colores = dict(zip(centros_costo_valores, colores))

# Crear figura con go.Bar
fig_bar = go.Figure(data=[
    go.Bar(
        x=costos_por_ceco.index,
        y=costos_por_ceco.values,
        marker_color=[ceco_colores.get(ceco, "#cccccc") for ceco in costos_por_ceco.index],  # usa color mapeado
        text=[f"${v:,.0f}" for v in costos_por_ceco.values],
        textposition="outside",
        hovertext=[f"{ceco}: ${v:,.0f}" for ceco, v in zip(costos_por_ceco.index, costos_por_ceco.values)],
        hoverinfo="text"
    )
])

# Personalizar layout
fig_bar.update_layout(
    title="Distribución de Costos por Centro de Costos",
    yaxis_title=None,
    xaxis_title=None,
    plot_bgcolor="rgba(0,0,0,0)",
    bargap=0.3,
    height=500
)

# Mostrar en Streamlit
st.plotly_chart(fig_bar, use_container_width=True)

# === Gráfico de torta ===

fig_pie = go.Figure(data=[
    go.Pie(
        labels=costos_por_ceco.index,
        values=costos_por_ceco.values,
        marker=dict(colors=[ceco_colores.get(ceco, "#cccccc") for ceco in costos_por_ceco.index]),
        textinfo="label+percent",
        hoverinfo="label+value+percent",
        hole=0.4 # 0 para torta completa, 0.4 para dona
    )
])

# Personalizar layout
fig_pie.update_layout(
    title="Proporción de costos por Centro de Costos",
    showlegend=True,
    height=500,
    plot_bgcolor="rgba(0,0,0,0)"
)

# Mostrar en Streamlit
st.plotly_chart(fig_pie, use_container_width=True)

# Elementos enalzados a cultivos:
    # * RRHH
    # * Agroquímicos
    # * Seguros:
        # * Solo sección cultivo
    # * Inversiones
    # * Servicios Externos MMOO



# INGRESOS POR CULTIVO (?)

# st.subheader("Distribución de Ingresos por Ítem")
# if not df_ingresos.empty and "item" in df_ingresos.columns:
#     ingresos_por_item = df_ingresos.groupby("item")["valor_bruto"].sum().sort_values(ascending=False)
#     st.bar_chart(ingresos_por_item, color="#008000")
