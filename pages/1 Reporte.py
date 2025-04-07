import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Reportes", layout="wide")
st.title("📊 Reporte General de Costos e Ingresos")

spreadsheet = st.session_state.get("spreadsheet")
if not spreadsheet:
    st.error("❌ No se pudo acceder al documento. Verifica la conexión en la página de Inicio.")
    st.stop()

# Cargar datos de las hojas de Google Sheets
try:
    costos_data = spreadsheet.worksheet("costos").get_all_records()
    ingresos_data = spreadsheet.worksheet("ingresos").get_all_records()
    df_costos = pd.DataFrame(costos_data)
    df_ingresos = pd.DataFrame(ingresos_data)
except Exception as e:
    st.error(f"❌ Error al cargar datos: {e}")
    st.stop()

# Convertir fechas a tipo datetime
for col in ["fecha_gasto", "fecha_ingreso"]:
    if col in df_costos.columns:
        df_costos[col] = pd.to_datetime(df_costos[col], format="%d/%m/%Y", errors="coerce")
    if col in df_ingresos.columns:
        df_ingresos[col] = pd.to_datetime(df_ingresos[col], format="%d/%m/%Y", errors="coerce")

# Calcular totales
total_costos = df_costos["valor_bruto"].sum()
total_ingresos = df_ingresos["valor_bruto"].sum()
balance = total_ingresos - total_costos

# Tarjetas resumen
st.subheader("Resumen General")
col1, col2, col3 = st.columns(3)
col1.metric("💸 Total de Costos", f"${total_costos:,.0f}".replace(",", "."), help="Suma de todos los costos")
col2.metric("💰 Total de Ingresos", f"${total_ingresos:,.0f}".replace(",", "."), help="Suma de todos los ingresos")
col3.metric("📈 Balance", f"${balance:,.0f}".replace(",", "."), delta=f"{(balance / total_costos * 100):.2f}%" if total_costos > 0 else "", help="Ingresos - Costos")

st.divider()

# Gráfico por ítem
st.subheader("Distribución de Costos por Ítem")
costos_por_item = df_costos.groupby("item")["valor_bruto"].sum().sort_values(ascending=False)
st.bar_chart(costos_por_item)

st.subheader("Distribución de Ingresos por Ítem")
ingresos_por_item = df_ingresos.groupby("item")["valor_bruto"].sum().sort_values(ascending=False)
st.bar_chart(ingresos_por_item)

st.divider()
st.subheader("Últimos Registros")
st.write("🟥 Últimos 5 costos registrados")
st.dataframe(df_costos.sort_values("id", ascending=False).head(5), use_container_width=True)

st.write("🟩 Últimos 5 ingresos registrados")
st.dataframe(df_ingresos.sort_values("id", ascending=False).head(5), use_container_width=True)
