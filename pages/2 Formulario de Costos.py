import streamlit as st
from datetime import datetime
import pytz

st.title("📋 Formulario de Registro de Costos")

spreadsheet = st.session_state.get("spreadsheet")
if not spreadsheet:
    st.error("❌ No se pudo acceder al documento. Verifica la conexión en la página principal.")
    st.stop

# Obtener la hoja de costos
sheet = spreadsheet.worksheet("costos")

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
    ceco_sheet = spreadsheet.worksheet("ceco")
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
    cultivo_sheet = spreadsheet.worksheet("cultivos")
    data = cultivo_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
    cultivo_list = [row["cultivo"] for row in data if row["cultivo"].strip()]
except Exception as e:
    st.error(f"❌ Error al cargar la lista de centro de cultivos: {e}")
    cultivo_list = []

# Condicional CECO
if ceco == "RRHH":                                                                                             # COLUMNA
    # st.subheader()
    cultivo = st.selectbox(                                                                                    # COLUMNA
        "Seleccione Cultivo",
        cultivo_list,
        index=None,
        placeholder="Cultivos"
    )
    # LISTA DE SUB-CATEGORIAS RRHH
        # Obtener lista dinámica desde la hoja 'rrhh'
    try:
        sub_rrhh_sheet = spreadsheet.worksheet("sub_rrhh")
        data = sub_rrhh_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
        sub_rrhh_list = [row["sub_rrhh"] for row in data if row["sub_rrhh"].strip()]
    except Exception as e:
        st.error(f"❌ Error al cargar la lista de subcategorias de RRHH: {e}")
        sub_rrhh_list = []

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

    cultivo = st.selectbox(                                                                                    # COLUMNA
        "Seleccione Cultivo",
        cultivo_list,
        index=None,
        placeholder="Cultivos"
    )

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

    # LISTA DE MAQUINAS
        # Obtener lista dinámica desde la hoja 'maquinas'
    try:
        maquinas_sheet = spreadsheet.worksheet("maquinas")
        data = maquinas_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
        maquinas_list = [row["maquina"] for row in data if row["maquina"].strip()]
    except Exception as e:
        st.error(f"❌ Error al cargar la lista de maquinas: {e}")
        maquinas_list = []

    maquina = st.selectbox(
        "Seleccione Maquinaria",
        maquinas_list,
        index=None,
        placeholder="Maquinaria"
    )

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
    elif sub_seguros == "Equipos":
        # LISTA DE MAQUINAS
        # Obtener lista dinámica desde la hoja 'maquinas'
        try:
            maquinas_sheet = spreadsheet.worksheet("maquinas")
            data = maquinas_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
            maquinas_list = [row["maquina"] for row in data if row["maquina"].strip()]
        except Exception as e:
            st.error(f"❌ Error al cargar la lista de maquinas: {e}")
            maquinas_list = []

        maquina = st.selectbox(
            "Seleccione Equipo",
            maquinas_list,
            index=None,
            placeholder="Equipo"
        )
    elif sub_seguros == "Cultivos":
        cultivo = st.selectbox(
            "Seleccione Cultivo",
            cultivo_list,
            index=None,
            placeholder="Cultivos"
        )

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
            "Seleccione sub-categoria",
            ["Preparación de Suelo", 
             "Agroquímico"],
             index=None,
             placeholder="Sub-categorias Preparación Previa"
        )
    
    else:

        cultivo = st.selectbox(
            "Seleccione Cultivo",
            cultivo_list,
            index=None,
            placeholder="Cultivos"
        )

elif ceco == "Servicio Externos MMOO":

    cultivo = st.selectbox(
        "Seleccione Cultivo",
        cultivo_list,
        index=None,
        placeholder="Cultivos"
    )

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

elif ceco == "Servicios Basicos":

    # (COMPLETAR)

elif ceco == "Combustibles":

    # (COMPLETAR)

elif ceco == "Gastos Varios / Otros":

    # (COMPLETAR)

else:

    # (COMPLETAR)


# # Tipo servicio (Petróleo, Energía, Agua, Otro)
# servicio = st.selectbox(
#     "Tipo Servicio",
#     ["Petróleo", "Energía", "Agua", "Otro"],
#     index=None,
#     placeholder="Seleccione tipo de servicio"
# )

st.divider()

st.subheader("Proveedores")

# Proveedores
try:
    # Obtener lista dinámica de proveedores desde la hoja 'proveedores'
    proveedores_sheet = spreadsheet.worksheet("proveedores")
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

st.subheader("Información Boleta/factura")

# N° Folio boleta/factura
numero_folio = st.number_input(
    "Número de Folio de Boleta/Factura",
    min_value=None,
    step=1,
    format="%d",
    placeholder="N° de boleta o factura"
)

# Fecha del Gasto
    # Fecha en la que se efectuó el gasto/compra/costo
fecha_gasto = st.date_input(
    "Fecha del Gasto o Compra",
    value="today",
    format="DD/MM/YYYY"
)

# Fecha de Emisión
    # Fecha de emisión de la boleta o factura
fecha_emision = st.date_input(
    "Fecha de Emisión Boleta/Factura",
    value="today",
    format="DD/MM/YYYY"
)

# Fecha de Vencimiento
fecha_vencimiento = st.date_input(
    "Fecha de Vencimiento Boleta/Factura",
    value="today",
    format="DD/MM/YYYY"
)

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
    # Primero validamos que los campos Descripción Gasto, Valor Bruto del Gasto, Ítem y Proveedor no estén vacíos
    errores = []

    if not descripcion.strip():
        errores.append("La descripción del gasto es obligatoria.")
    if valor_bruto <= 0:
        errores.append("El valor bruto debe ser mayor que cero.")
    if not ceco:
        errores.append("Debe seleccionar un ítem.")
    if not servicio:
        errores.append("Debe seleccionar un servicio.")
    if not proveedor_final:
        errores.append("Debe seleccionar o ingresar un proveedor.")
    if numero_folio < 0:
        errores.append("N° de folio debe ser un número positivo.")

    if errores:
        for err in errores:
            st.warning(err)

    else:
        # Si todo está en orden se procede a agregar los datos a la planilla
        try:
            # Obtener los encabezados (primera fila de la hoja)
            headers = sheet.row_values(1)
            # Definir zona horaria de Santiago
            zona_horaria_chile = pytz.timezone('Chile/Continental')
            # Obtener la hora actual en la zona horaria de Santiago
            fecha_hora_actual = datetime.now(zona_horaria_chile).strftime("%d/%m/%Y %H:%M:%S")    # datetime se transforma a string
            # Obtener el nuevo índice (número de fila - 1 para no contar el encabezado)
            num_filas_existentes = len(sheet.get_all_values())
            nuevo_index = num_filas_existentes  # Si hay encabezado, el índice empieza desde 1

            # Armar diccionario con los datos usando los nombres de las columnas
            registro = {
                "id" : nuevo_index,
                "fecha_envio_form": fecha_hora_actual,
                "descripcion": descripcion,
                "valor_bruto": valor_bruto,
                "valor_neto": valor_neto,
                "iva": iva,
                "item": ceco,
                "servicio": servicio,
                "proveedor": proveedor_final,
                "numero_folio": numero_folio,
                "fecha_gasto": fecha_gasto.strftime("%d/%m/%Y"),                # datetime se transforma a string
                "fecha_emision": fecha_emision.strftime("%d/%m/%Y"),            # datetime se transforma a string
                "fecha_vencimiento": fecha_vencimiento.strftime("%d/%m/%Y"),    # datetime se transforma a string
                "comentarios": comentario
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

    # # Mostrar éxito si fue guardado
    # if st.session_state.get("registro_guardado"):
    #     st.success("¡Registro guardado con éxito!")
    #     st.session_state["registro_guardado"] = False  # Limpiar para no mostrarlo siempre