import gspread
from google.oauth2.service_account import Credentials
import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Registro de Costos e Ingresos", layout="centered")

st.title("Bienvenido al Sistema de Registro")
st.subheader("Selecciona una opción para comenzar:")

col1, col2, col3 = st.columns(3)

button_style = """
    <style>
    div.stButton > button {
        width: 100%;
    }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)

with col1:
    if st.button("Ir a Reporte"):
        st.switch_page("pages/1 Reporte.py")

with col2:
    if st.button("Ir a Formulario de Costos"):
        st.switch_page("pages/2 Formulario de Costos.py")

with col3:
    if st.button("Ir a Formulario de Ingresos"):
        st.switch_page("pages/3 Formulario de Ingresos.py")

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

# 🔽 Nueva sección: vencimientos "Por definir"

def obtener_filas_con_por_definir(spreadsheet):
    hojas = [
        "rrhh", "agroquimicos", "maquinaria", "administracion", "seguros",
        "inversiones", "servicios_externos", "servicios_basicos", "combustibles", "gastos_varios"
    ]
    columnas_objetivo = [
        "fecha_vencimiento_30", "fecha_vencimiento_60",
        "fecha_vencimiento_90", "fecha_vencimiento_120"
    ]

    columnas_a_mostrar = [
        "hoja_origen", "descripcion", "valor_bruto", "fecha_emision",
        "fecha_vencimiento_30", "tipo_pago_30",
        "fecha_vencimiento_60", "tipo_pago_60",
        "fecha_vencimiento_90", "tipo_pago_90",
        "fecha_vencimiento_120", "tipo_pago_120"
    ]

    resultados = []

    for hoja in hojas:
        try:
            ws = spreadsheet.worksheet(hoja)
            registros = ws.get_all_records()
            df = pd.DataFrame(registros)
            df["hoja_origen"] = hoja

            columnas_presentes = [col for col in columnas_objetivo if col in df.columns]
            if not columnas_presentes:
                continue

            filtro = df[columnas_presentes].apply(lambda fila: "Por definir" in fila.values, axis=1)
            df_filtrado = df[filtro]

            if not df_filtrado.empty:
                columnas_validas = [col for col in columnas_a_mostrar if col in df_filtrado.columns]
                resultados.append(df_filtrado[columnas_validas])

        except Exception as e:
            print(f"Error en hoja {hoja}: {e}")
            continue

    return pd.concat(resultados, ignore_index=True) if resultados else pd.DataFrame()

# Mostrar solo estas columnas:
# columnas_a_mostrar = ["centro_costo", "descripcion", "valor_bruto", "fecha_emision", "fecha_vencimiento_30", "tipo_pago_30", "fecha_vencimiento_60", "tipo_pago_60", "fecha_vencimiento_90", "tipo_pago_90", "fecha_vencimiento_120", "tipo_pago_120"]
# ¿Se deberia incluir: [ "numero_folio", "subcategoria", "cultivo", "comentario"]?

st.divider()
st.markdown("### Vencimientos pendientes por definir")

df_alertas = obtener_filas_con_por_definir(st.session_state["spreadsheet"])
if not df_alertas.empty:
    st.dataframe(df_alertas)
else:
    st.info("No hay vencimientos marcados como 'Por definir'.")