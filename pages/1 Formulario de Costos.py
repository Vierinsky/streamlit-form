import streamlit as st
from datetime import datetime
import pytz

st.title("Formulario de Registro de Costos")

spreadsheet = st.session_state.get("spreadsheet")
if not spreadsheet:
    st.error("❌ No se pudo acceder al documento. Verifica la conexión en la página principal.")
    st.stop

# Obtener la hoja de costos
sheet = spreadsheet.worksheet("costos")

# Inputs
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

# Item/Cultivo/Centro de costos del gasto
    # Agregar opción para customizar lista de ítems (?)
item = st.selectbox(
    "Ítem", 
    ['Aseo y Ornato', 'Campo General', 'Choclo', 'Frambuesas', 'Papas', 'Pasto', 'Peonías'], 
    index=None, 
    placeholder="Seleccione ítem o centro de costos")

# Proveedores
try:
    # Obtener lista dinámica de proveedores desde la hoja 'proveedores'
    proveedores_sheet = spreadsheet.worksheet("proveedores")
    data = proveedores_sheet.get_all_records()  # Devuelve una lista de diccionarios, ignorando encabezado
    proveedores_list = [row["proveedores"] for row in data if row["proveedores"].strip()]
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
    if not item:
        errores.append("Debe seleccionar un ítem.")
    if not proveedor_final:
        errores.append("Debe seleccionar o ingresar un proveedor.")
    if numero_folio < 0:
        errores.append("N° de folio debe ser un número positivo")

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
                "fecha_envio": fecha_hora_actual,
                "descripcion": descripcion,
                "valor_bruto": valor_bruto,
                "valor_neto": valor_neto,
                "iva": iva,
                "item": item,
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
            st.session_state["registro_guardado"] = True  # Marcar que se guardó con éxito

            # st.success("¡Registro guardado con éxito!")

            # Solo si se usó un nuevo proveedor y no está en la lista
            if not proveedor_seleccionado and nuevo_proveedor.strip() and nuevo_proveedor.strip() not in proveedores_list:
                proveedores_sheet.append_row(["", nuevo_proveedor.strip()])

        except Exception as e:
            st.error(f"❌ Error al guardar el registro en Google Sheets: {e}")
            st.session_state["registro_guardado"] = False  # Resetear si falló

    # Mostrar éxito si fue guardado
    if st.session_state.get("registro_guardado"):
        st.success("¡Registro guardado con éxito!")
        st.session_state["registro_guardado"] = False  # Limpiar para no mostrarlo siempre