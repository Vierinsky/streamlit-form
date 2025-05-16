# Formulario de Sueldos

# TODO:
#   - En la división de días y sueldo por cultivo ¿Se puede decidir a que cultivo se le asigna que suma de dinero?

from datetime import datetime
from google.oauth2.service_account import Credentials
import gspread
import json
import os
import pandas as pd
import pytz
import re
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

# === Calculo leyes sociales ===

# Porcentajes leyes sociales
    # REVISAR (pq lo hizo DonGepe)
TASAS = {
    "Indefinido": {
        "afp": 0.10,
        "salud": 0.07,
        "cesantia_trabajador": 0.006,
        "cesantia_empleador": 0.024,
        "sis": 0.0153,
        "atep": 0.0093
    },
    "Plazo Fijo": {
        "afp": 0.10,
        "salud": 0.07,
        "cesantia_trabajador": 0.0,
        "cesantia_empleador": 0.03,
        "sis": 0.0153,
        "atep": 0.0093
    },
    "Honorarios": {
        "afp": 0.0,
        "salud": 0.0,
        "cesantia_trabajador": 0.0,
        "cesantia_empleador": 0.0,
        "sis": 0.0,
        "atep": 0.0
    }
}

def calcular_leyes_sociales(sueldo_bruto: int, tipo_contrato: str) -> dict:
    """
    Calcula el desglose de leyes sociales para un trabajador en Chile según su tipo de contrato.

    Args:
        sueldo_bruto (int): Sueldo bruto mensual del trabajador.
        tipo_contrato (str): Tipo de contrato del trabajador. Debe ser una clave válida en el diccionario TASAS.

    Returns:
        dict: Un diccionario con el monto correspondiente a cada componente de las leyes sociales, 
              según las tasas establecidas para el tipo de contrato. Si el tipo de contrato no existe 
              en TASAS, se retorna un diccionario vacío.
    
    Ejemplo de retorno:
        {
            "afp": 10000,
            "salud": 7000,
            "seguro_cesantia": 3000
        }
    """
    tasas = TASAS.get(tipo_contrato	, {})
    detalle = {}

    for item, tasa in tasas.items():
        detalle[item] = round(sueldo_bruto * tasa)
    
    detalle["total_aportes"] = sum(detalle.values())
    
    return detalle

# === Formulario Principal ===

st.title("📋 Formulario de Registro de Sueldos")

# ✅ Mostrar mensaje de éxito si se acaba de guardar un registro
if st.session_state.get("registro_guardado"):
    st.toast("Registro guardado con éxito", icon="✅")
    st.session_state["registro_guardado"] = False

# == Validación RUT == INCORPORAR A SECCIÓN VALIDACIONES

def validar_rut(rut: str) -> bool:
    """
    Valida si un RUT chileno es correcto. El RUT puede venir con puntos y guion.

    Args:
        rut (str): RUT en formato string. Ejemplo válido: "12.345.678-5"

    Returns:
        bool: True si el RUT es válido, False si no lo es.
    
    La validación se hace usando el algoritmo del módulo 11, que consiste en:
    - Multiplicar cada dígito del cuerpo del RUT por factores decrecientes del 2 al 7 (en bucle).
    - Calcular el resto de la suma de esos productos dividido por 11.
    - Obtener el dígito verificador y compararlo con el ingresado.
    """

    # 1. Limpiar el RUT: quitar puntos y guion, y convertir a mayúsculas
    rut = rut.replace(".", "").replace("-", "").upper()

    # 2. Verificar que tenga el formato correcto: 7 u 8 dígitos + un dígito o 'K'
    if not re.match(r'^\d{7,8}[0-9K]$', rut):
        return False

    # 3. Separar cuerpo y dígito verificador
    cuerpo = rut[:-1]
    verificador = rut[-1]

    # 4. Calcular el dígito verificador usando el algoritmo del módulo 11
    suma = 0
    multiplicador = 2
    for d in reversed(cuerpo):
        suma += int(d) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1

    resto = 11 - (suma % 11)
    digito = {11: '0', 10: 'K'}.get(resto, str(resto))

    # 5. Comparar el dígito calculado con el ingresado
    return digito == verificador

# === Formulario: Datos del trabajador ===

st.markdown("### Información del Trabajador")

# Campo para nombre
nombre_trabajador = st.text_input("Nombre completo del trabajador")

# Tipo de documento
tipo_documento = st.selectbox("Tipo de documento", ["RUT", "Pasaporte", "Otro"])

# Campo para ingresar número
numero_documento = st.text_input("Número de documento", placeholder="Ej: 12.345.678-5")

# Validación si es RUT
if tipo_documento == "RUT" and numero_documento:
    if not validar_rut(numero_documento):
        st.warning("⚠️ El RUT ingresado no es válido. Revise el formato y el dígito verificador.")

# === Ingrese Fecha ===
st.divider()
# Fecha de Emisión
    # Fecha de emisión de la factura
fecha_hoy_chile = datetime.now(pytz.timezone('Chile/Continental')).date()

fecha_sueldo = st.date_input(
    "Ingrese Fecha en que se realiza el pago",
    value=fecha_hoy_chile,
    format="DD/MM/YYYY"
)

# === Días trabajados por cultivo / Ceco ===

def get_fresh_spreadsheet():
    """
    Devuelve una conexión activa a Google Sheets. Si ya existe en session_state la reutiliza.

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
def cargar_hoja(nombre_hoja: str) -> list[dict]:
    """
    Lee todos los registros de una hoja de Google Sheets y cachea el resultado.

    Args:
        nombre_hoja (str): nombre de la pestaña a leer.

    Returns:
        list: Lista de diccionarios.
    """
    sheet = get_fresh_spreadsheet().worksheet(nombre_hoja)
    return sheet.get_all_records()

# LISTA DE CULTIVOS
    # Obtener lista dinámica de cultivos desde la hoja 'cultivos'
try:
    data = cargar_hoja("cultivos")
    cultivo_list = [r["cultivo"] for r in data if r["cultivo"].strip()]
except Exception as e:
    st.error(f"❌ Error al cargar la lista de centro de cultivos: {e}")
    cultivo_list = []

st.divider()
# Multiselect para elegir cultivos
cultivos_trabajados = st.multiselect(
    "Seleccione área o cultivo en que trabajó",     # ¿Comentar que es (Selección Múltiple)?
    cultivo_list,
    placeholder="Escoja una o más opciones"
)

# Diccionario para almacenar días trabajados por cultivo
dias_por_cultivo = {}

for cultivo in cultivos_trabajados:
    # Obtener días trabajados por cultivo
    dias_trabajados = st.number_input(
        f"Días trabajados en {cultivo}", 
        min_value=1, 
        step=1,
        format="%d"
        )
    
    # Añadir cultivo al dicc junto con sus días trabajados
    dias_por_cultivo[cultivo] = dias_trabajados

# Convertir el diccionario en lista de tuplas
datos = [{"Cultivo": cultivo, "Días": dias} for cultivo, dias in dias_por_cultivo.items()]

# Armando dataframe para días trabajados por cultivo
df_dias_por_cultivo = pd.DataFrame(datos)

if dias_por_cultivo != {}:
    st.markdown("### Resúmen días trabajados por cultivo")
    st.table(df_dias_por_cultivo)

# === Sueldo Bruto ===
st.divider()

tipo_contrato = st.radio("Seleccione tipo de contrato", ["Indefinido", "Plazo Fijo", "Honorarios"], horizontal=True)

sueldo_bruto = st.number_input(
    "Sueldo bruto",
    min_value=0, 
    step=1,
    format="%d"
)

# === Gratificaciones (Se suman despúes de las leyes sociales) ===
gratificaciones = st.number_input(
    "Agregue gratificaciones si aplican",
    min_value=0, 
    step=1,
    format="%d",
    help="Las gratificaciones se suman después de las leyes sociales al sueldo bruto"
)

remuneracion_total = sueldo_bruto + gratificaciones

leyes = calcular_leyes_sociales(sueldo_bruto, tipo_contrato)

sueldo_neto = sueldo_bruto - sum([
    leyes['afp'],
    leyes['salud'],
    leyes['cesantia_trabajador'], 
    leyes['cesantia_empleador'], 
    leyes['sis'], 
    leyes['atep']
    ])

porcentaje_afp = str(round(TASAS[tipo_contrato]['afp'] * 100, 2))
porcentaje_salud = str(round(TASAS[tipo_contrato]['salud'] * 100, 2))
porcentaje_cestrab = str(round(TASAS[tipo_contrato]['cesantia_trabajador'] * 100, 2))
porcentaje_cesemp = str(round(TASAS[tipo_contrato]['cesantia_empleador'] * 100, 2))
porcentaje_sis = str(round(TASAS[tipo_contrato]['sis'] * 100, 2))
porcentaje_atep = str(round(TASAS[tipo_contrato]['atep'] * 100, 2))


# === Tabla Resumen Desglose LLSS y Sueldo ===

data = {
    "Concepto": [
        "Sueldo Neto",
        f"Previsión (AFP)",
        f"Salud (Fonasa/Isapre)",
        f"Cesantía (Trabajador)",
        f"Cesantía (Empleador)",
        f"SIS",
        f"ATEP",
        "Gratificaciones",
        "Sueldo Bruto"
    ],
    "Porcentaje" : ["", 
                    f"{porcentaje_afp}%", 
                    f"{porcentaje_salud}%", 
                    f"{porcentaje_cestrab}%", 
                    f"{porcentaje_cesemp}%", 
                    f"{porcentaje_sis}%", 
                    f"{porcentaje_atep}%",
                    "",
                    ""
    ],
    "Monto CLP": [
        sueldo_neto, leyes['afp'], leyes['salud'],
        leyes['cesantia_trabajador'], leyes['cesantia_empleador'], leyes['sis'], leyes['atep'], gratificaciones , remuneracion_total # Se suman gratificaciones a sueldo final
    ]
}

# Insertar fila "Leyes Sociales"
indices_llss = [1, 2, 3, 4, 5, 6] # INdices de los conceptos de leyes sociales
monto_llss = sum(data["Monto CLP"][i] for i in indices_llss)

insert_pos = 7 # Justo antes de "Gratificaciones"

data["Concepto"].insert(insert_pos, "Leyes Sociales")
data["Porcentaje"].insert(insert_pos, "")
data["Monto CLP"].insert(insert_pos, monto_llss)

# Crear Dataframe
df_montos = pd.DataFrame(data)

# Función para formatear montos con miles . y decimales ,
def formato_monto(valor):
    return f"${valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Función para formatear porcentajes (ya en decimal: 0.153 → 15,30%)
def formato_porcentaje(valor_str):
    try:
        valor = float(valor_str.strip('%'))
        return f"{valor:.2f}".replace(".", ",") + "%"
    except:
        return valor_str  # por si viene vacío o malformado

# Aplica formato
df_montos["Monto CLP"] = df_montos["Monto CLP"].apply(formato_monto)
df_montos["Porcentaje"] = df_montos["Porcentaje"].apply(formato_porcentaje)

if sueldo_bruto != 0:
    # st.subheader("Detalle de Descuentos y Leyes Sociales")
    st.markdown("### Detalle Leyes sociales")
    
    # Filtrar filas por Concepto
    filtro = (df_montos["Concepto"].isin(["Previsión (AFP)", "Salud (Fonasa/Isapre)", "Cesantía (Trabajador)", "Cesantía (Empleador)", "SIS", "ATEP"]))
    df_resumen_leyes = df_montos.loc[filtro, ["Concepto", "Porcentaje", "Monto CLP"]]
    
    #  Mostrar tabla
    st.write(f"**Tipo de contrato:** {tipo_contrato}")
    st.table(df_resumen_leyes)
    
    # Filtrar filas por Concepto
    total_llss = {
        "Concepto" : "Total Leyes Sociales", 
        "Monto CLP" : df_montos[df_montos["Concepto"].isin(["Previsión (AFP)", "Salud (Fonasa/Isapre)", "Cesantía (Trabajador)", "Cesantía (Empleador)", "SIS", "ATEP"])]["Monto CLP"].sum()
    }
    
    filtro = df_montos["Concepto"].isin(["Sueldo Neto", "Leyes Sociales","Gratificaciones", "Sueldo Bruto"])
    df_resumen_sueldo = df_montos.loc[filtro, ["Concepto", "Monto CLP"]]

    df_resumen_sueldo["Concepto"] = df_resumen_sueldo["Concepto"].replace('Sueldo Bruto', 'Remuneración Total')

    # Mostrar tabla
    st.markdown("### Resumen Sueldo")
    st.table(df_resumen_sueldo)

# === Resúmen ===

if not df_dias_por_cultivo.empty and "Días" in df_dias_por_cultivo.columns:
    # Asegurarse de que días y sueldo neto estén en valores numéricos
    df_dias_por_cultivo["Días"] = pd.to_numeric(df_dias_por_cultivo["Días"], errors="coerce").fillna(0).astype(int)

    # Calcular total de días trabajados
    total_dias = df_dias_por_cultivo["Días"].sum()

    # Calcular sueldo proporcional
    if total_dias > 0:
        df_dias_por_cultivo["monto_CLP"] = df_dias_por_cultivo["Días"] / total_dias * (remuneracion_total)
        df_dias_por_cultivo["monto_CLP"] = df_dias_por_cultivo["monto_CLP"].round(0).astype(int)
    else:
        df_dias_por_cultivo["monto_CLP"] = 0

    # Formateo visual
    df_dias_por_cultivo["monto_CLP_fmt"] = df_dias_por_cultivo["monto_CLP"].apply(lambda x: f"${x:,.0f}".replace(",", "."))
    df_display_dias_cultivo = df_dias_por_cultivo[["Cultivo", "Días", "monto_CLP_fmt"]].rename(columns={"monto_CLP_fmt": "Sueldo Bruto"})

    if sueldo_bruto > 0:
        st.markdown("### Resumen sueldo y días trabajados por cultivo")
        st.table(df_display_dias_cultivo)

# === Tipo de Pago y Banco ===

# Con que banco se paga
# IDEA: Que el usuario ingrese cuantos pagos(vencimientos) y estos se desplieguen respectivamente
        # Esta idea puede ser para otros formularios.

# 1. FORMA DE PAGO: EFECTIVO, DEPOSITO, etc
st.divider()

tipo_pago = st.radio("Seleccione Tipo de Pago", ["Efectivo", "Depósito en Cuenta Bancaria", "Vale Vista"], horizontal=True)

# Nota: para pago en efectivo la empresa debe emitir un comprobante firmado por el trabajador como respaldo.

# 2. SI ES DEPOSITO O Vale Vista CON QUE BANCO SE PAGÓ

if tipo_pago in ["Depósito en Cuenta Bancaria", "Vale Vista"]:
    data = cargar_hoja("tipo_pagos")
    bancos_lista = [r["tipo_pago"] for r in data if r["tipo_pago"].strip()]
    banco = st.selectbox("Seleccione Banco", bancos_lista, index=None, placeholder="Banco")

# === Comentarios ===
# Comentario opcional del usuario
st.divider()
comentario = st.text_area(
    "Comentario (opcional)", 
    placeholder="Agregue una nota o comentario"
)

# IMPORTANTE
    # COMPLETAR LO QUE IRÁ EN LA PLANILLA
        # Falta:
            # días trabajados por cultivo que será su propia planilla
            # leyes sociales (¿Agregar una por una o como total?)
    # [nombre_trabajador, numero_documento, cultivos_trabajados, tipo_contrato, sueldo_bruto, leyes, gratificaciones, remuneracion_total, tipo_pago, banco]

# === Validación ===

# Necesito validar
# [nombre_trabajador, numero_documento, cultivos_trabajados, tipo_contrato, sueldo_bruto, gratificaciones, tipo_pago, banco]

# TODO: De esta página deberían salir 2 planillas:
            # Una donde aparezca el sueldo completo del trabajador.
            # Otra donde aparezca el sueldo dividido por cultivo trabajado.
                # (¿Es necesario esto? Quizás baste con un DataFrame que sea utilizado por dentro por los gráficos)

#   MODIFICAR A LA REALIDAD DEL FORMULARIO DE SUELDOS.

# # Inicializar estado si no existe
# if "registro_guardado" not in st.session_state:
#     st.session_state["registro_guardado"] = False

# if st.button("Guardar Registro"):
    # ——— INICIO SECCIÓN DE VALIDACIÓN ———
    # errores = []

    # # 1) Campos generales obligatorios
    # if not descripcion.strip():
    #     errores.append("La descripción del gasto es obligatoria.")
    # if valor_bruto <= 0:
    #     errores.append("El valor bruto debe ser mayor que cero.")
    # if not ceco:
    #     errores.append("Debe seleccionar un Centro de Costos.")

    # else:
    #     # Si todo está en orden se procede a agregar los datos a la planilla

    #     def preparar_registro(sheet_name):
    #         """
    #         Prepara una hoja específica de Google Sheets para registrar un nuevo dato.

    #         Args:
    #             sheet_name (str): Nombre de la hoja.

    #         Returns:
    #             sheet (gspread.Worksheet): Objeto Worksheet correspondiente.
    #             headers (list): Lista de nombres de columna.
    #             nuevo_index (int): Número de fila a insertar (sin contar encabezado).
    #             fecha_hora_actual (str): Timestamp en formato %d/%m/%Y %H:%M:%S.
    #         """
    #         sheet = get_fresh_spreadsheet().worksheet(sheet_name)
    #         headers = sheet.row_values(1)

    #         zona_horaria_chile = pytz.timezone('Chile/Continental')
    #         fecha_hora_actual = datetime.now(zona_horaria_chile).strftime("%d/%m/%Y %H:%M:%S")
    #         nuevo_index = len(sheet.get_all_values())

    #         return sheet, headers, nuevo_index, fecha_hora_actual

# === Botón de guardado ===

# 1. Ingrese sueldo bruto
#       - Que muestre desglose.
#       - Que permita dividir el sueldo según días trabajados en x cultivo.
#       - Que se agregue nombre del trabajador. 

# 2. Desea agregar Gratificaciones?

# Nota: 
#   ¿Debe haber sección banco también?
#   ¿Si se tiene a un trabajador contratado se debe auto agregar todos los meses su sueldo?
#   ¿Se necesita info más detallada del trabajador? Ej: RUT u otros.

# 3. Mostrar resúmen
# 4. Sección "Comentario"
# 4. Enviar formulario