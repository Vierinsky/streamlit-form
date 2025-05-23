# Formulario de Sueldos

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
    # TODO: REVISAR
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
    Valida un RUT chileno asegurando formato y veracidad del dígito verificador.

    Args:
        rut (str): RUT ingresado por el usuario. Puede tener puntos y guión (ej. "12.345.678-5").

    Returns:
        bool: True si el RUT es válido, False si no lo es.
    """

    # 1. Limpiar el RUT: quitar puntos, guiones, espacios, pasar a mayúsculas
    rut = rut.replace(".", "").replace("-", "").strip().upper()

    # 2. Verificar largo mínimo y máximo
    if len(rut) < 8 or len(rut) > 9:
        return False

    # 3. Separar cuerpo (todo menos último dígito) y dígito verificador (último carácter)
    cuerpo, dv = rut[:-1], rut[-1]

    # 4. Validar que el cuerpo sea numérico
    if not cuerpo.isdigit():
        return False

    # 5. Calcular el dígito verificador esperado
    suma = 0
    factor = 2

    for c in reversed(cuerpo):
        suma += int(c) * factor
        factor = 2 if factor == 7 else factor + 1  # ciclo: 2→7

    dv_esperado = 11 - (suma % 11)
    if dv_esperado == 11:
        dv_esperado = "0"
    elif dv_esperado == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(dv_esperado)

    # 6. Comparar dígito ingresado con el esperado
    return dv == dv_esperado

# === Formulario: Datos del trabajador ===

st.markdown("### Información del Trabajador")

def get_df_trabajadores():
    """
    Carga la hoja 'trabajadores' como DataFrame con validación de columnas esenciales.

    - Si la hoja está vacía o faltan columnas clave, retorna un DataFrame vacío pero con los encabezados esperados.
    - Normaliza el formato de la columna 'numero_documento' para evitar errores por comillas u otros formatos desde Google Sheets.

    Returns:
        pd.DataFrame: DataFrame con los datos de trabajadores, incluyendo columnas:
                      ['id_trabajador', 'nombre_trabajador', 'tipo_documento', 'numero_documento']
    """
    df = cargar_dataframe("trabajadores")
    if "numero_documento" not in df.columns or "nombre_trabajador" not in df.columns:
        return pd.DataFrame(columns=[
            "id_trabajador",
            "nombre_trabajador",
            "tipo_documento",
            "numero_documento"
        ])
    return df

# Cargar la hoja "trabajadores" como DataFrame
df_trabajadores = get_df_trabajadores()

# Validar que:
# 1. El DataFrame no esté vacío (tiene al menos una fila de datos)
# 2. Contenga la columna "numero_documento"
if not df_trabajadores.empty and "numero_documento" in df_trabajadores.columns:
    
    # Si cumple ambas condiciones, normaliza el formato de número de documento
    # Google Sheets a veces lo guarda como texto con comilla inicial: '12345678
    df_trabajadores["numero_documento"] = (
        df_trabajadores["numero_documento"]
        .astype(str)     # Asegura que todos sean strings
        .str.strip()     # Elimina espacios al inicio y final
        .str.lstrip("'") # Elimina comilla simple inicial si existe
    )

else:
    # Si no hay datos o falta la columna, crea un DataFrame vacío
    # pero con las columnas esperadas para evitar errores más adelante
    df_trabajadores = pd.DataFrame(columns=[
        "id_trabajador",
        "nombre_trabajador",
        "tipo_documento",
        "numero_documento"
    ])


if df_trabajadores.empty:
    # Envía mensaje en caso de que en planilla "trabajadores" no haya ningún trabajador registrado 
    st.warning("⚠️ No hay trabajadores registrados aún. Ingrese un nuevo trabajador.")
    lista_trabajadores = ["Nuevo trabajador"]
else:
    # Crea una lista de texto con formato "nombre - número_documento"
    # Agrega una opción para registrar uno nuevo
    lista_trabajadores = ["Nuevo trabajador"] + (df_trabajadores["nombre_trabajador"].astype(str) + " - " + df_trabajadores["numero_documento"].astype(str)).tolist()

# Selectbox para que el usuario elija
seleccion = st.selectbox("Seleccione trabajador", options=lista_trabajadores)

if seleccion == "Nuevo trabajador":
    nombre_trabajador = st.text_input("Nombre del trabajador")
    tipo_documento = st.selectbox("Tipo de documento", ["RUT", "Pasaporte", "Otro"])
    numero_documento = st.text_input("Número de documento (sin puntos ni guión)")

    # Validación inmediata de RUT con feedback visible
    if tipo_documento == "RUT" and numero_documento:
        rut_input = numero_documento.replace(".", "").replace("-", "").strip().upper()
        if len(rut_input) < 8 or len(rut_input) > 9:
            st.warning("⚠️ El RUT debe tener entre 8 y 9 caracteres.")
        elif not rut_input[:-1].isdigit():
            st.warning("⚠️ El cuerpo del RUT debe contener solo números.")
        else:
            # Cálculo de dígito verificador
            cuerpo, dv = rut_input[:-1], rut_input[-1]
            suma = 0
            factor = 2
            for c in reversed(cuerpo):
                suma += int(c) * factor
                factor = 2 if factor == 7 else factor + 1
            dv_esperado = 11 - (suma % 11)
            if dv_esperado == 11:
                dv_esperado = "0"
            elif dv_esperado == 10:
                dv_esperado = "K"
            else:
                dv_esperado = str(dv_esperado)
            if dv != dv_esperado:
                st.warning(f"⚠️ Dígito verificador incorrecto. Se esperaba '{dv_esperado}'.")
    
else:
    datos = seleccion.split(" - ")
    nombre_trabajador = datos[0]
    numero_documento = datos[1]
    tipo_documento = df_trabajadores[df_trabajadores["numero_documento"] == numero_documento]["tipo_documento"].values[0]


# Limpiar formato (estandarización para validaciones y almacenamiento)
numero_documento_limpio = numero_documento.replace(".", "").replace("-", "").strip().upper()

# === Ingrese Fecha ===
st.divider()
# Fecha de Emisión
    # Fecha de emisión de la factura
fecha_hoy_chile = datetime.now(pytz.timezone('Chile/Continental')).date()

fecha_sueldo = st.date_input(
    "Ingrese Fecha en que se realiza el pago",
    value=fecha_hoy_chile,
    format="DD/MM/YYYY"
).strftime("%d/%m/%Y")

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

# Tabla de días por cultivo
# if dias_por_cultivo != {}:
#     st.markdown("### Resúmen días trabajados por cultivo")
#     st.table(df_dias_por_cultivo)

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

tipo_pago = st.radio("Seleccione Tipo de Pago", ["Efectivo", "Caja Chica","Depósito en Cuenta Bancaria", "Vale Vista"], horizontal=True)

# Nota: para pago en efectivo la empresa debe emitir un comprobante firmado por el trabajador como respaldo.

banco = ""  # Valor de Banco es empty por defecto

if tipo_pago in ["Depósito en Cuenta Bancaria", "Vale Vista"]:
    data = cargar_hoja("tipo_pagos")
    bancos_lista = [
        r["tipo_pago"]
        for r in data 
        if r["tipo_pago"].strip() and r["tipo_pago"] not in ["Efectivo", "Caja Chica"]
    ]
    banco = st.selectbox("Seleccione Banco", bancos_lista, index=None, placeholder="Banco")

# === Comentarios ===
# Comentario opcional del usuario
st.divider()
comentario = st.text_area(
    "Comentario (opcional)", 
    placeholder="Agregue una nota o comentario"
)

# === Botón de guardado ===

if st.button("Guardar Registro"):
    # === Validación ===

    # Necesito validar:
    # [nombre_trabajador, numero_documento_limpio, cultivos_trabajados, tipo_contrato, sueldo_bruto, gratificaciones, tipo_pago, banco]
   
    errores = []

    # Validar nombre
    if not nombre_trabajador.strip():
        errores.append("Debe ingresar el nombre del trabajador.")

    # Validar documento
    if not numero_documento_limpio.strip():
        errores.append("Debe ingresar un número de documento.")
    elif tipo_documento == "RUT" and not validar_rut(numero_documento_limpio):
        errores.append("El RUT ingresado no es válido.")

    # Validación para otros documentos
    elif tipo_documento in ["Pasaporte", "Otro"] and len(numero_documento_limpio.strip()) < 5:
        errores.append("El número de documento parece demasiado corto.")

    # Validar cultivo(s)
    if not cultivos_trabajados:
        errores.append("Debe seleccionar al menos un cultivo trabajado.")
    
    # Valida que total de días trabajados sea mayor a 0
    total_dias = sum(dias_por_cultivo.values())
    if total_dias <= 0:
        errores.append("Debe ingresar al menos un día trabajado en algún cultivo.")

    # Validar que campos de días no esten en blanco
    if any(dias <= 0 for dias in dias_por_cultivo.values()):
        errores.append("Debe ingresar días válidos para cada cultivo seleccionado.")

    # Validar tipo de contrato
    if not tipo_contrato:
        errores.append("Debe seleccionar el tipo de contrato.")

    # Validar sueldo bruto
    if sueldo_bruto <= 0:
        errores.append("El sueldo bruto debe ser mayor a 0.")

    # Validar gratificaciones
    if gratificaciones < 0:
        errores.append("Las gratificaciones no pueden ser negativas.")

    # Validar tipo de pago
    if not tipo_pago:
        errores.append("Debe seleccionar una forma de pago.")

    # Validar banco si el pago requiere banco
    if tipo_pago not in ["Efectivo", "Caja Chica"] and not banco:
        errores.append("Debe seleccionar un banco para pagos que no sean en efectivo o caja chica.")


    if errores:
        for err in errores: st.warning(err)
    else:
        try:

            def obtener_o_crear_id_trabajador(nombre: str, numero_documento: str, tipo_documento: str, spreadsheet) -> int:
                """
                Busca si un trabajador ya existe en la hoja 'trabajadores' por su número de documento.
                Si lo encuentra, devuelve su id_trabajador. Si no, lo agrega como nuevo y retorna el nuevo ID asignado.
                
                Esta versión no depende del orden de las columnas en la hoja, siempre que existan las siguientes:
                'id_trabajador', 'nombre_trabajador', 'numero_documento', 'tipo_documento'.

                Args:
                    nombre (str): Nombre completo del trabajador.
                    numero_documento (str): Número de documento (sin puntos ni guión en el caso del RUT).
                    tipo_documento (str): Tipo de documento ('RUT', 'Pasaporte', etc).
                    spreadsheet (gspread.Spreadsheet): Conexión activa al archivo de Google Sheets.

                Returns:
                    int: El ID único del trabajador.
                """
                hoja = spreadsheet.worksheet("trabajadores")
                registros = hoja.get_all_records()
                headers = hoja.row_values(1)

                # Buscar si ya existe el trabajador por número de documento
                for fila in registros:
                    if str(fila.get("numero_documento", "")).strip() == numero_documento.strip():
                        return int(fila.get("id_trabajador"))

                # Si no existe, crear un nuevo ID (siguiente fila disponible)
                nuevo_id = len(registros) + 1

                fila_dict = {
                    "id_trabajador": nuevo_id,
                    "nombre_trabajador": nombre.strip(),
                    "numero_documento": numero_documento.strip(),
                    "tipo_documento": tipo_documento.strip()
                }

                # Armar la fila en el orden correcto de los headers
                nueva_fila = [fila_dict.get(col, "") for col in headers]
                hoja.append_row(nueva_fila)

                # Agrega la fila
                # (ya se agregó en la línea anterior)

                # ✅ Validación inmediata: vuelve a cargar los registros y verifica si el trabajador fue agregado
                registros_actualizados = hoja.get_all_records()
                trabajador_nuevo = next(
                    (r for r in registros_actualizados if str(r.get("numero_documento", "")).strip() == numero_documento.strip()), 
                    None
                )

                if trabajador_nuevo:
                    st.success(f"✅ Trabajador '{trabajador_nuevo.get('nombre_trabajador', '')}' agregado correctamente.")
                else:
                    st.error("❌ No se encontró el trabajador recién agregado en la hoja.")

                return nuevo_id


            sheet_sueldos = spreadsheet.worksheet("sueldos")
            headers_sueldos = sheet_sueldos.row_values(1)
            fecha_envio = datetime.now(pytz.timezone('Chile/Continental')).strftime("%d/%m/%Y %H:%M:%S")
            nuevo_id = len(sheet_sueldos.get_all_values())
            id_trabajador = obtener_o_crear_id_trabajador(nombre_trabajador, numero_documento_limpio, tipo_documento,spreadsheet)

    # TODO: * Crear "sueldos_por_cultivo":
    #           * Columnas = [id_trabajador,nombre_trabajador,numero_documento,fecha_sueldo,cultivo,dias_trabajados,remuneracion_cultivo] 
    #           * id_trabajador debería ser igual a una columna que se llame "id_trabajador" en "sueldos" que a su vez reconozca si se ingresa un trabajador ingresado anteriormente
    #               Para lo cual se necesitaría una base de datos de trabajadores.
    #       * Crear "trabajadores":
    #           * Columnas: [id_trabajador,nombre_trabajador, tipo_documento, numero_documento]
    #           * Puede que se necesite agregar nuevas columnas según necesidades de la empresa

            afp = round(leyes.get('afp', 0))
            salud = round(leyes.get('salud', 0))
            cesantia_trabajador = round(leyes.get('cesantia_trabajador', 0))
            cesantia_empleador = round(leyes.get('cesantia_empleador', 0))
            sis = round(leyes.get('sis', 0))
            atep = round(leyes.get('atep', 0))

            registro_sueldos = {
                "id" : nuevo_id,
                "fecha_envio" : fecha_envio,
                "id_trabajador": id_trabajador,
                "nombre_trabajador" : nombre_trabajador,
                "tipo_documento" : tipo_documento,
                "numero_documento" : numero_documento_limpio,
                "fecha_sueldo" : fecha_sueldo,
                "total_dias_trabajados" : total_dias,
                # "cultivos_trabajados" : cultivos_trabajados,      # Decidí sacar esta columna de esta planilla ya que esta info ya se usa en la planilla "sueldos_por_cultivo"
                "tipo_contrato" : tipo_contrato,
                "afp" : afp,
                "salud" : salud,
                "cesantia_trabajador" : cesantia_trabajador,
                "cesantia_empleador" : cesantia_empleador,
                "sis" : sis,
                "atep" : atep,
                "total_llss" : sum([afp, salud, cesantia_trabajador, cesantia_empleador, sis, atep]),
                "gratificaciones": gratificaciones,
                "sueldo_neto": sueldo_neto,
                "sueldo_bruto": sueldo_bruto,
                "remuneracion_total": remuneracion_total,
                "tipo_pago" : tipo_pago,
                "banco": banco,
                "comentarios": comentario
            }

            fila_final = [registro_sueldos.get(col, "") for col in headers_sueldos]
            sheet_sueldos.append_row(fila_final)

            # === Guardar en hoja "sueldos_por_cultivo" ===

            sheet_cultivo = spreadsheet.worksheet("sueldos_por_cultivo")
            headers_cultivo = sheet_cultivo.row_values(1)
            nuevo_id = len(sheet_cultivo.get_all_values())

            for cultivo, dias in dias_por_cultivo.items():
                proporcion = dias / total_dias if total_dias > 0 else 0
                remuneracion_cultivo = round(remuneracion_total * proporcion)       # REVISAR SI SE GUARDA LA SUMA CORRECTA

                registro_cultivo = {
                    "id": nuevo_id,
                    "id_trabajador": id_trabajador,
                    "nombre_trabajador" : nombre_trabajador,
                    "fecha_sueldo": fecha_sueldo,
                    "cultivo": cultivo,
                    "dias_trabajados": dias,
                    "remuneracion_cultivo": remuneracion_cultivo
                }

                fila = [registro_cultivo.get(col, "") for col in headers_cultivo]
                sheet_cultivo.append_row(fila)
                nuevo_id += 1  # Para que cada fila tenga un ID único

            st.session_state["registro_guardado"] = True
            st.cache_data.clear()  # 🔄 Limpiar cache de datos para forzar recarga actualizada
            st.toast("Registro guardado con éxito", icon="✅")      # TODO: No se muestra mensaje de guardado con éxito CORREGIR
            st.markdown("""
                <meta http-equiv="refresh" content="0">
            """, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ Error al guardar el registro en Google Sheets: {e}")

# Variables de columnas de planilla "sueldos":
    # [nombre_trabajador, numero_documento_limpio, cultivos_trabajados, tipo_contrato, sueldo_bruto, leyes, gratificaciones, remuneracion_total, tipo_pago, banco]
