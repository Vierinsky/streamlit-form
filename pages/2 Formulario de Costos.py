import streamlit as st
from datetime import datetime
import pytz

# Diccionario de hojas de la planilla
    # Cambiar key en caso de modificaciones

HOJAS_GOOGLE_SHEETS = { 
    # Hojas principales por CECO
    "RRHH": "rrhh",
    "Agroquimico": "agroquimico",
    "Maquinaria": "maquinaria",
    "Administracion": "administracion",
    "Seguros": "seguros",
    "Inversiones": "inversiones",
    "Servicio Externos MMOO": "servicio_externos_mmoo",
    "Servicios Básicos": "servicios_basicos",
    "Combustibles": "combustibles",
    "Gastos Varios / Otros": "gastos_varios",

    # Hojas auxiliares
    "proveedores": "proveedores",
    "clientes": "clientes",         # Esto es para el Formulario de Ingresos
    "ceco": "ceco",
    "cultivos": "cultivos",
    "maquinas": "maquinas"
}

st.title("📋 Formulario de Registro de Costos")

spreadsheet = st.session_state.get("spreadsheet")
if not spreadsheet:
    st.error("❌ No se pudo acceder al documento. Verifica la conexión en la página principal.")
    st.stop

# # Obtener la hoja de costos
# sheet = spreadsheet.worksheet("costos")

# ✅ Mostrar mensaje de éxito si se acaba de guardar un registro
if st.session_state.get("registro_guardado"):
    st.toast("Registro guardado con éxito", icon="✅")
    st.session_state["registro_guardado"] = False

# Inputs

st.divider()

st.subheader("Información General")

# Descripción Gasto
descripcion = st.text_input(
    "Descripción del Gasto", 
    placeholder='"Pago Iva y 20% restante", "Compra Touchdown IQ 500 20 L", "Asesoria"')

# Valor bruto del Gasto - solo valores tipo int
valor_bruto = st.number_input(
    "Valor Bruto del Gasto/Compra (IVA incluido)", 
    min_value=0, 
    step=1,
    format="%d"
)
# Calculo IVA y valor neto
iva = valor_bruto * 0.19
valor_neto = valor_bruto - iva

# Formateo visual con separador de miles (solo display opcional)
monto_formateado = f"{valor_bruto:,}".replace(",", ".")  # convierte 10000 → "10.000"
st.write(f"Monto ingresado: ${monto_formateado}")

st.divider()

st.subheader("Centro de Costos")

# CENTRO DE COSTOS
# LISTA DE CENTRO DE COSTOS
    # Obtener lista dinámica de centro de costos desde la hoja 'ceco'
try:
    ceco_sheet = spreadsheet.worksheet(HOJAS_GOOGLE_SHEETS["ceco"])
    data = ceco_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
    ceco_list = [row["ceco"] for row in data if row["ceco"].strip()]
except Exception as e:
    st.error(f"❌ Error al cargar la lista de centro de costos: {e}")
    ceco_list = []

ceco = st.selectbox(
    "Seleccione Centro de Costos", 
    ceco_list,
    index=None, 
    placeholder="Centro de Costos")

# LISTA DE CULTIVOS
    # Obtener lista dinámica de cultivos desde la hoja 'cultivos'
try:
    cultivo_sheet = spreadsheet.worksheet(HOJAS_GOOGLE_SHEETS["cultivos"])
    data = cultivo_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
    cultivo_list = [row["cultivo"] for row in data if row["cultivo"].strip()]
except Exception as e:
    st.error(f"❌ Error al cargar la lista de centro de cultivos: {e}")
    cultivo_list = []

# Definir función que despliega selectbox de cultivos
def seleccionar_cultivo(cultivo_list):
    """
    Muestra un menú desplegable obligatorio para que el usuario seleccione un cultivo.

    Args:
        cultivo_list (list): Lista de nombres de cultivos disponibles.

    Returns:
        str: Cultivo seleccionado por el usuario.
    """
    return st.selectbox(
        "Seleccione Cultivo",
        cultivo_list,
        index=None,
        placeholder="Cultivos"
    )

# LISTA DE MAQUINAS
    # Obtener lista dinámica desde la hoja 'maquinas'
try:
    maquinas_sheet = spreadsheet.worksheet(HOJAS_GOOGLE_SHEETS["maquinas"])
    data = maquinas_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
    maquinas_list = [row["maquina"] for row in data if row["maquina"].strip()]
except Exception as e:
    st.error(f"❌ Error al cargar la lista de maquinas: {e}")
    maquinas_list = []

def seleccionar_maquina(maquinas_list):
    """
    Muestra un selector desplegable para elegir una máquina desde una lista.

    Args:
        maquinas_list: Lista de máquinas disponibles.

    Returns:
        La máquina seleccionada o None si no se selecciona ninguna.
    """
    return st.selectbox(
        "Seleccione Maquinaria",
        maquinas_list,
        index=None,
        placeholder="Maquinaria"
    )



# Condicional CECO
if ceco == "RRHH":                                                                                             # COLUMNA
    # st.subheader()
    cultivo = seleccionar_cultivo(cultivo_list)

    sub_rrhh = st.selectbox(                                                                                  # COLUMNA
        "Seleccione sub-categoria RRHH",
        ["Sueldo administrativo", 
        "Sueldo operativo", 
        "Prevención", 
        "Leyes sociales", 
        "Capacitación", 
        "Bonos", 
        "Viaticos", 
        "Aguinaldos"],
        index=None,
        placeholder="Sub-categorias RRHH"
    )    
    # DESPUÉS DE RRHH ¿APLICA CONTINUAR CON SECCIÓN PROVEEDOR?

elif ceco == "Agroquimico":                                                                                   # COLUMNA

    cultivo = seleccionar_cultivo(cultivo_list)

    sub_agroquimico = st.selectbox(
        "Seleccione sub-categoria Agroquímicos",
        ["Fertilizante", "Fungicida", "Insectida", "Herbicida"],
        index=None,
        placeholder="Sub-categorias Agroquímicos"
    )

elif ceco == "Maquinaria":

    sub_maquinaria = st.selectbox(
        "Seleccione sub-categoria Maquinaria",
        ["Mantenimiento", "Reparación", "Mejora", "Servicio a Terceros"],
        index=None,
        placeholder="Sub-categorias Maquinaria"
    )

    maquina = seleccionar_maquina(maquinas_list)

elif ceco == "Administracion":
    # LISTA DE ADMINISTRACIÓN
        # Obtener lista dinámica desde la hoja 'sub_admin'
    try:
        sub_admin_sheet = spreadsheet.worksheet("sub_admin")
        data = sub_admin_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
        sub_admin_list = [row["sub_admin"] for row in data if row["sub_admin"].strip()]
    except Exception as e:
        st.error(f"❌ Error al cargar la lista de sub-categorias de Administración: {e}")
        sub_admin_list = []
    
    sub_admin = st.selectbox(
        "Seleccione sub-categoria Administración",
        ["Asesorias", "Subscripciones", "Viajes", "Form 29"],
        index=None,
        placeholder="Sub-categorias Administración"
    )

elif ceco == "Seguros":

    sub_seguros = st.selectbox(
        "Seleccione sub-categoria Seguros",
        ["Transporte", "Equipos", "Infraestructura", "Cultivos"],
        index=None,
        placeholder="Sub-categorias Seguros"
    )

    if sub_seguros == "Transporte":
        
        transporte = st.selectbox(
            "Seleccione Tipo de Transporte",
            ["Importación", "Exportación", "Carga Nacional"],
            index=None,
            placeholder="Tipo de Transporte"
        )

        cultivo = None
        maquina = None

    elif sub_seguros == "Equipos":

        maquina = seleccionar_maquina(maquinas_list)

        transporte = None

    elif sub_seguros == "Infraestructura":

        maquina = None
        cultivo = None
        transporte = None

    elif sub_seguros == "Cultivos":
        cultivo = seleccionar_cultivo(cultivo_list)

        maquina = None
        transporte = None

elif ceco == "Inversiones":
    # # LISTA DE SUB-CATEGORIA INVERSIONES
    #     # Obtener lista dinámica desde la hoja 'sub_inverison'
    # try:
    #     sub_inv_sheet = spreadsheet.worksheet("sub_inverison")
    #     data = sub_inv_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
    #     sub_inv_list = [row["sub_inverison"] for row in data if row["sub_inverison"].strip()]
    # except Exception as e:
    #     st.error(f"❌ Error al cargar la lista de sub-categorias de Seguros: {e}")
    #     sub_inv_list = []

    sub_inv = st.selectbox(
        "Seleccione Inversión",
        ["Maquinaria", 
         "Infraestructura", 
         "Equipos", 
         "Preparación Previa"],
        index=None,
        placeholder= "Sub-categorias Inverisión"
    )
    
    if sub_inv == "Preparación Previa":

        prep_prev = st.selectbox(
            "Seleccione Preparación Previa",
            ["Preparación de Suelo", 
             "Agroquímico"],
             index=None,
             placeholder="Sub-categorias Preparación Previa"
        )
        
        cultivo = None # Preguntar si "Preparación Previa" debe ir enlazada a un cultivo
    
    else:

        cultivo = seleccionar_cultivo(cultivo_list)

        prep_prev = None

elif ceco == "Servicio Externos MMOO":

    cultivo = seleccionar_cultivo(cultivo_list)

    servicios_externos = st.selectbox(
        "Seleccione Servicio Externo",
        ["Cosecha",
         "Selección",
         "Plantación",
         "Limpieza",
         "Aseo y ornato",
         "Otros"],
         index=None,
         placeholder="Servicios externos"
    )

elif ceco == "Servicios Básicos":

    servicios_basicos = st.selectbox(
        "Seleccione Servicio Básico",
        ["Agua", "Luz", "Gas", "Luz2 (Riego)"],
        index=None,
        placeholder="Servicios Básicos"
    )

elif ceco == "Combustibles":
    
    combustibles = st.selectbox(
        "Seleccione Combustible",
        ["Petróleo", "Bencina", "Energia"],
        index=None,
        placeholder="Combustibles"
    )

# Aqui iría "Gastos Varios / Otros"


# # Tipo servicio (Petróleo, Energía, Agua, Otro)
# servicio = st.selectbox(
#     "Tipo Servicio",
#     ["Petróleo", "Energía", "Agua", "Otro"],
#     index=None,
#     placeholder="Seleccione tipo de servicio"
# )

if ceco == "RRHH":  # Si se selecciona RRHH no se necesita especificar proveedor 

    proveedor_final = None

else:

    st.divider()

    st.subheader("Proveedores")

    # Proveedores
    try:
        # Obtener lista dinámica de proveedores desde la hoja 'proveedores'
        proveedores_sheet = spreadsheet.worksheet(HOJAS_GOOGLE_SHEETS["proveedores"])
        data = proveedores_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
        proveedores_list = [row["proveedor"] for row in data if row["proveedor"].strip()]
    except Exception as e:
        st.error(f"❌ Error al cargar la lista de proveedores: {e}")
        proveedores_list = []

    proveedor_seleccionado = st.selectbox(
        "Proveedor", 
        proveedores_list, 
        index=None, 
        placeholder="Seleccione proveedor"
    )

    # Limpiar campo de texto si se seleccionó un proveedor de la lista
    if proveedor_seleccionado and st.session_state.get("nuevo_proveedor"):
        st.session_state["nuevo_proveedor"] = ""

    # Input de nuevo proveedor
    nuevo_proveedor = st.text_input(
        "¿Proveedor no está en la lista? Escriba nuevo proveedor. De lo contrario dejar en blanco",
        placeholder="Nombre del nuevo proveedor",
        key="nuevo_proveedor"
    )

    # Decidir qué valor usar
    proveedor_final = nuevo_proveedor.strip() if nuevo_proveedor else proveedor_seleccionado

    # Agrega nuevo proveedor a la lista y le genera un id
    if not proveedor_seleccionado and nuevo_proveedor.strip() and nuevo_proveedor.strip() not in proveedores_list:
        num_filas_proveedores = len(proveedores_sheet.get_all_values())
        nuevo_id_proveedor = num_filas_proveedores  # Asumiendo que fila 1 es encabezado
        proveedores_sheet.append_row([nuevo_id_proveedor, nuevo_proveedor.strip()])

    # Priorizar proveedor seleccionado
    proveedor_final = proveedor_seleccionado if proveedor_seleccionado else nuevo_proveedor.strip()

st.divider()

st.subheader("Información Factura")

# N° Folio factura
numero_folio = st.text_input(
    "Número de Factura (opcional)",
    placeholder='Dejar en blanco si no aplica'
)

# Procesar el valor: si está vacío, lo tratamos como "null"
numero_folio = numero_folio.strip() if numero_folio.strip() else "null"

# Fecha de Emisión
    # Fecha de emisión de la factura
fecha_emision = st.date_input(
    "Fecha de Emisión Factura",
    value="today",
    format="DD/MM/YYYY"
)

# Para definir fecha de vencimiento del pago (30, 60, 120 días)

def fecha_vencimiento_input(dias):
    
    """
    Muestra un input condicional para seleccionar una fecha de vencimiento, o marcarla como 
    'No aplica' o 'Por definir', según el número de días especificado.

    Args:
        dias (int): Número de días del vencimiento (ej. 30, 60, 120). Se usa para identificar el campo y personalizar el texto.

    Returns:
        str or None: 
            - Si se selecciona "Ingresar fecha", retorna la fecha seleccionada como string con formato "DD/MM/YYYY".
            - Si se selecciona "Por definir", retorna la cadena "Por definir".
            - Si se selecciona "No aplica", retorna `None` (para que se interprete como valor nulo en el backend).
    """
        
    opcion = st.selectbox(
        f"Vencimiento a {dias} días",
        ["Ingresar fecha", "No aplica", "Por definir"],
        key=f"opcion_{dias}"
    )

    if opcion == "Ingresar fecha":
        fecha = st.date_input(
            f"Fecha para {dias} días",
            key=f"fecha_{dias}",
            format="DD/MM/YYYY"
        )
        return fecha.strftime("%d/%m/%Y") # Devuelve fecha en formato str
    elif opcion == "Por definir":
        return "Por definir"
    else:
        return None # No Aplica -> se guarda como valor null

# Invocar para los tres plazos
vencimiento_30 = fecha_vencimiento_input(30)
vencimiento_60 = fecha_vencimiento_input(60)
vencimiento_120 = fecha_vencimiento_input(120)

st.divider()

# Comentario opcional del usuario
comentario = st.text_area(
    "Comentario (opcional)", 
    placeholder="Agregue una nota o comentario"
)

# Botón de guardar registro

# Inicializar estado si no existe
if "registro_guardado" not in st.session_state:
    st.session_state["registro_guardado"] = False

if st.button("Guardar Registro"):
    # ——— INICIO SECCIÓN DE VALIDACIÓN ———
    errores = []

    # 1) Campos generales obligatorios
    if not descripcion.strip():
        errores.append("La descripción del gasto es obligatoria.")
    if valor_bruto <= 0:
        errores.append("El valor bruto debe ser mayor que cero.")
    if not ceco:
        errores.append("Debe seleccionar un Centro de Costos.")

    # 2) Validar subcampos según CECO
    if ceco == "RRHH":
        if not sub_rrhh:
            errores.append("Debe seleccionar una sub-categoría de RRHH.")
        if not cultivo:
            errores.append("Debe seleccionar un cultivo para RRHH.")
    elif ceco == "Agroquimico":
        if not sub_agroquimico:
            errores.append("Debe seleccionar una sub-categoría de Agroquímicos.")
        if not cultivo:
            errores.append("Debe seleccionar un cultivo para Agroquímicos.")
    elif ceco == "Maquinaria":
        if not sub_maquinaria:
            errores.append("Debe seleccionar una sub-categoría de Maquinaria.")
        if not maquina:
            errores.append("Debe seleccionar una Maquinaria.")
    elif ceco == "Administracion":
        if not sub_admin:
            errores.append("Debe seleccionar una sub-categoría de Administración.")
    elif ceco == "Seguros":
        if not sub_seguros:
            errores.append("Debe seleccionar una sub-categoría de Seguros.")
        # si Transporte/Equipos/Cultivos… validarlos aquí como lo hicimos arriba
    elif ceco == "Inversiones":
        if not sub_inv:
            errores.append("Debe seleccionar una sub-categoría de Inversiones.")
        # y así para las demás ramas…
    # no validamos nada especial para "Servicios Básicos", "Combustibles" o "Gastos Varios / Otros"

    # 3) Proveedor (solo si aplica)
    if ceco != "RRHH":
        if not proveedor_final:
            errores.append("Debe seleccionar o ingresar un proveedor.")

    # 4) Número de factura (puede estar en blanco o “null”)
    if numero_folio not in ("", "null"):
        if not numero_folio.isdigit():
            errores.append("El número de factura debe ser numérico o dejarse en blanco.")

    # Mostrar advertencias
    if errores:
        for err in errores:
            st.warning(err)
    # ——— FIN SECCIÓN DE VALIDACIÓN ———


    else:
        # Si todo está en orden se procede a agregar los datos a la planilla

        def preparar_registro(spreadsheet, sheet_name):
            """
            Prepara una hoja específica de Google Sheets para registrar un nuevo dato.

            Args:
                spreadsheet: Objeto Spreadsheet conectado.
                sheet_name (str): Nombre de la hoja.

            Returns:
                sheet: Objeto Worksheet correspondiente.
                headers (list): Lista de nombres de columna.
                nuevo_index (int): Número de fila a insertar (sin contar encabezado).
                fecha_hora_actual (str): Timestamp en formato %d/%m/%Y %H:%M:%S.
            """
            sheet = spreadsheet.worksheet(sheet_name)
            headers = sheet.row_values(1)

            zona_horaria_chile = pytz.timezone('Chile/Continental')
            fecha_hora_actual = datetime.now(zona_horaria_chile).strftime("%d/%m/%Y %H:%M:%S")
            nuevo_index = len(sheet.get_all_values())

            return sheet, headers, nuevo_index, fecha_hora_actual

        try:
            # "RRHH"
            if ceco == "RRHH":

                sheet, headers, nuevo_index, fecha_hora_actual = preparar_registro(spreadsheet, HOJAS_GOOGLE_SHEETS["RRHH"])

                # Armar diccionario con los datos usando los nombres de las columnas
                registro = {
                    "id" : nuevo_index,
                    "fecha_envio_form": fecha_hora_actual,
                    "descripcion": descripcion,
                    "valor_bruto": valor_bruto,
                    "valor_neto": valor_neto,
                    "iva": iva,
                    "centro_costo": ceco,
                    "subcategoria": sub_rrhh,
                    # "proveedor": proveedor_final,     # NO APLICA EN RRHH
                    "cultivo" : cultivo,
                    "numero_folio": numero_folio,       # ¿APLICA?
                    "fecha_emision": fecha_emision.strftime("%d/%m/%Y"),            # datetime se transforma a string
                    "fecha_vencimiento_30": vencimiento_30,
                    "fecha_vencimiento_60": vencimiento_60,
                    "fecha_vencimiento_120": vencimiento_120,
                    "comentario": comentario
                }

            # "Agroquimico"
            elif ceco == "Agroquimico":

                sheet, headers, nuevo_index, fecha_hora_actual = preparar_registro(spreadsheet, HOJAS_GOOGLE_SHEETS["Agroquimico"])

                registro = {
                    "id" : nuevo_index,
                    "fecha_envio_form": fecha_hora_actual,
                    "descripcion": descripcion,
                    "valor_bruto": valor_bruto,
                    "valor_neto": valor_neto,
                    "iva": iva,
                    "centro_costo": ceco,
                    "subcategoria": sub_agroquimico,
                    "proveedor": proveedor_final,
                    "cultivo" : cultivo,
                    "numero_folio": numero_folio,
                    "fecha_emision": fecha_emision.strftime("%d/%m/%Y"),            # datetime se transforma a string
                    "fecha_vencimiento_30": vencimiento_30,
                    "fecha_vencimiento_60": vencimiento_60,
                    "fecha_vencimiento_120": vencimiento_120,
                    "comentario": comentario
                }

            # "Maquinaria"
            elif ceco == "Maquinaria":

                sheet, headers, nuevo_index, fecha_hora_actual = preparar_registro(spreadsheet, HOJAS_GOOGLE_SHEETS["Maquinaria"])

                # Armar diccionario con los datos usando los nombres de las columnas
                registro = {
                    "id" : nuevo_index,
                    "fecha_envio_form": fecha_hora_actual,
                    "descripcion": descripcion,
                    "valor_bruto": valor_bruto,
                    "valor_neto": valor_neto,
                    "iva": iva,
                    "centro_costo": ceco,
                    "subcategoria": sub_maquinaria,
                    "maquina": maquina,
                    "proveedor": proveedor_final,
                    # "cultivo" : cultivo,                    # No Aplica
                    "numero_folio": numero_folio,
                    "fecha_emision": fecha_emision.strftime("%d/%m/%Y"),            # datetime se transforma a string
                    "fecha_vencimiento_30": vencimiento_30,
                    "fecha_vencimiento_60": vencimiento_60,
                    "fecha_vencimiento_120": vencimiento_120,
                    "comentario": comentario
                }

            # "Administracion"
            elif ceco == "Administracion":
                sheet, headers, nuevo_index, fecha_hora_actual = preparar_registro(spreadsheet, HOJAS_GOOGLE_SHEETS["Administracion"])

                # Armar diccionario con los datos usando los nombres de las columnas
                registro = {
                    "id" : nuevo_index,
                    "fecha_envio_form": fecha_hora_actual,
                    "descripcion": descripcion,
                    "valor_bruto": valor_bruto,
                    "valor_neto": valor_neto,
                    "iva": iva,
                    "centro_costo": ceco,
                    "subcategoria": sub_admin,
                    "proveedor": proveedor_final,
                    # "cultivo" : cultivo,                    # No Aplica
                    "numero_folio": numero_folio,
                    "fecha_emision": fecha_emision.strftime("%d/%m/%Y"),            # datetime se transforma a string
                    "fecha_vencimiento_30": vencimiento_30,
                    "fecha_vencimiento_60": vencimiento_60,
                    "fecha_vencimiento_120": vencimiento_120,
                    "comentario": comentario
                }

            # "Seguros"
            elif ceco == "Seguros":
                sheet, headers, nuevo_index, fecha_hora_actual = preparar_registro(spreadsheet, HOJAS_GOOGLE_SHEETS["Seguros"])

                # Armar diccionario con los datos usando los nombres de las columnas
                registro = {
                    "id" : nuevo_index,
                    "fecha_envio_form": fecha_hora_actual,
                    "descripcion": descripcion,
                    "valor_bruto": valor_bruto,
                    "valor_neto": valor_neto,
                    "iva": iva,
                    "centro_costo": ceco,
                    "subcategoria": sub_seguros,
                    "proveedor": proveedor_final,
                    "transporte": transporte,
                    "maquina" : maquina,
                    "cultivo" : cultivo,
                    "numero_folio": numero_folio,
                    "fecha_emision": fecha_emision.strftime("%d/%m/%Y"),            # datetime se transforma a string
                    "fecha_vencimiento_30": vencimiento_30,
                    "fecha_vencimiento_60": vencimiento_60,
                    "fecha_vencimiento_120": vencimiento_120,
                    "comentario": comentario
                }

            # "Inversiones"
            elif ceco == "Inversiones":
                sheet, headers, nuevo_index, fecha_hora_actual = preparar_registro(spreadsheet, HOJAS_GOOGLE_SHEETS["Inversiones"])

                # Armar diccionario con los datos usando los nombres de las columnas
                registro = {
                    "id" : nuevo_index,
                    "fecha_envio_form": fecha_hora_actual,
                    "descripcion": descripcion,
                    "valor_bruto": valor_bruto,
                    "valor_neto": valor_neto,
                    "iva": iva,
                    "centro_costo": ceco,
                    "subcategoria": sub_inv,
                    "preparacion_previa" : prep_prev,
                    "cultivo" : cultivo,
                    "numero_folio": numero_folio,
                    "fecha_emision": fecha_emision.strftime("%d/%m/%Y"),            # datetime se transforma a string
                    "fecha_vencimiento_30": vencimiento_30,
                    "fecha_vencimiento_60": vencimiento_60,
                    "fecha_vencimiento_120": vencimiento_120,
                    "comentario": comentario
                }
            # "Servicio Externos MMOO"

            elif ceco == "Servicio Externos MMOO":
                sheet, headers, nuevo_index, fecha_hora_actual = preparar_registro(spreadsheet, HOJAS_GOOGLE_SHEETS["Servicio Externos MMOO"])

                # Armar diccionario con los datos usando los nombres de las columnas
                registro = {
                    "id" : nuevo_index,
                    "fecha_envio_form": fecha_hora_actual,
                    "descripcion": descripcion,
                    "valor_bruto": valor_bruto,
                    "valor_neto": valor_neto,
                    "iva": iva,
                    "centro_costo": ceco,
                    "subcategoria": servicios_externos,
                    "cultivo" : cultivo,
                    "numero_folio": numero_folio,
                    "fecha_emision": fecha_emision.strftime("%d/%m/%Y"),            # datetime se transforma a string
                    "fecha_vencimiento_30": vencimiento_30,
                    "fecha_vencimiento_60": vencimiento_60,
                    "fecha_vencimiento_120": vencimiento_120,
                    "comentario": comentario
                }

            # "Servicios Básicos"
            elif ceco == "Servicios Básicos":
                sheet, headers, nuevo_index, fecha_hora_actual = preparar_registro(spreadsheet, HOJAS_GOOGLE_SHEETS['Servicios Básicos'])

                # Armar diccionario con los datos usando los nombres de las columnas
                registro = {
                    "id" : nuevo_index,
                    "fecha_envio_form": fecha_hora_actual,
                    "descripcion": descripcion,
                    "valor_bruto": valor_bruto,
                    "valor_neto": valor_neto,
                    "iva": iva,
                    "centro_costo": ceco,
                    "subcategoria": servicios_basicos,
                    "numero_folio": numero_folio,
                    "fecha_emision": fecha_emision.strftime("%d/%m/%Y"),            # datetime se transforma a string
                    "fecha_vencimiento_30": vencimiento_30,
                    "fecha_vencimiento_60": vencimiento_60,
                    "fecha_vencimiento_120": vencimiento_120,
                    "comentario": comentario
                }
            # "Combustibles"
            elif ceco == "Combustibles":
                sheet, headers, nuevo_index, fecha_hora_actual = preparar_registro(spreadsheet, HOJAS_GOOGLE_SHEETS["Combustibles"])

                # Armar diccionario con los datos usando los nombres de las columnas
                registro = {
                    "id" : nuevo_index,
                    "fecha_envio_form": fecha_hora_actual,
                    "descripcion": descripcion,
                    "valor_bruto": valor_bruto,
                    "valor_neto": valor_neto,
                    "iva": iva,
                    "centro_costo": ceco,
                    "subcategoria": combustibles,
                    "numero_folio": numero_folio,
                    "fecha_emision": fecha_emision.strftime("%d/%m/%Y"),            # datetime se transforma a string
                    "fecha_vencimiento_30": vencimiento_30,
                    "fecha_vencimiento_60": vencimiento_60,
                    "fecha_vencimiento_120": vencimiento_120,
                    "comentario": comentario
                }
       
            # "Gastos Varios / Otros"
            elif ceco == "Gastos Varios / Otros":
                sheet, headers, nuevo_index, fecha_hora_actual = preparar_registro(spreadsheet, HOJAS_GOOGLE_SHEETS["Gastos Varios / Otros"])

                # Armar diccionario con los datos usando los nombres de las columnas
                registro = {
                    "id" : nuevo_index,
                    "fecha_envio_form": fecha_hora_actual,
                    "descripcion": descripcion,
                    "valor_bruto": valor_bruto,
                    "valor_neto": valor_neto,
                    "iva": iva,
                    "centro_costo": ceco,
                    # "subcategoria": combustibles,     # No Aplica
                    "numero_folio": numero_folio,
                    "fecha_emision": fecha_emision.strftime("%d/%m/%Y"),            # datetime se transforma a string
                    "fecha_vencimiento_30": vencimiento_30,
                    "fecha_vencimiento_60": vencimiento_60,
                    "fecha_vencimiento_120": vencimiento_120,
                    "comentario": comentario
                }

            # Crear la fila final según el orden real de los encabezados
            fila_final = [registro.get(col, "") for col in headers]
            # Insertar la fila
            sheet.append_row(fila_final)

            # ✅ Marcar éxito y refrescar
            st.session_state["registro_guardado"] = True  # Marcar que se guardó con éxito

            # Solo si se usó un nuevo proveedor y no está en la lista
            if not proveedor_seleccionado and nuevo_proveedor.strip() and nuevo_proveedor.strip() not in proveedores_list:
                proveedores_sheet.append_row(["", nuevo_proveedor.strip()])

            # 🔄 Refrescar la app
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error al guardar el registro en Google Sheets: {e}")
            st.session_state["registro_guardado"] = False  # Resetear si falló
