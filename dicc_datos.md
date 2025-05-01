Nota: 
* Agregar Hoja ingresos
* Traducir dicc al inglés
* Arreglar tablas markdown de este archivo
* Agregar si columna acepta o no "null"

Hojas: ["rrhh", "agroquimicos", "maquinaria", "administracion", "seguros", "inversiones", "servicios_externos", "servicios_basicos", "combustibles", "gastos_varios"]


# Hoja "rrhh"

Columna | Tipo | Definición
"id" | int | Id único
"fecha_envio_form" | str | Fecha en que el usuario guardó el formulario. Nota: datetime transformado a str. Ej: 'dd/mm/yyyy hh:mm:ss'
"descripcion" | str | Nota corta que describe el costo
"valor_bruto" | int | Valor del costo IVA incluido
"valor_neto" | int | Valor del costo sin IVA
"iva" | int | IVA del costo
"centro_costo" | str | Centro de costos al que pertenece el costo. Valor fijo: "RRHH"
"subcategoria" | str | Subcategoría de RRHH. Valores posibles: ["Sueldo administrativo", "Sueldo operativo", "Prevención", "Leyes sociales", "Capacitación", "Bonos", "Viaticos", "Aguinaldos"]
"cultivo" | str | Cultivo al que se asocia el costo. Valores posibles: [Aseo y ornato, Campo General, Choclo, Frambuesas, Papas, Pasto, Peonías] o "N/A"
"numero_folio" | str | Número de factura (es un valor numérico). Valores posibles: '1234567' o 'N/A'
"fecha_emision" | str | Fecha en que fue emitida la factura. Valores posibles: datetime(str) o 'N/A'. Nota: datetime transformado a str
"fecha_vencimiento_30" | str | Fecha de vencimiento a 30 días. Valores posibles: datetime(str), 'Por definir' o 'N/A'
"tipo_pago_30" | str | Tipo de pago para factura con vencimiento a 30 días. Valores posibles: ["Banco de Chile", "Banco Edwards", "Banco Bice", "Caja Chica", "Efectivo"] o 'N/A'
"fecha_vencimiento_60" | str | Fecha de vencimiento a 60 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_60" | str | Tipo de pago para factura con vencimiento a 60 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_90" | str | Fecha de vencimiento a 90 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_90" | str | Tipo de pago para factura con vencimiento a 90 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_120" | str | Fecha de vencimiento a 120 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_120" | str | Tipo de pago para factura con vencimiento a 120 días. Mismos valores que "tipo_pago_30"
"comentario" | str | Comentario opcional sobre el costo. Valores posibles: str o None

# Hoja "agroquimicos"

Columna | Tipo | Definición
"id" | int | Id único
"fecha_envio_form" | str | Fecha en que el usuario guardó el formulario. Nota: datetime transformado a str. Ej: 'dd/mm/yyyy hh:mm:ss'
"descripcion" | str | Nota corta que describe el costo
"valor_bruto" | int | Valor del costo IVA incluido
"valor_neto" | int | Valor del costo sin IVA
"iva" | int | IVA del costo
"centro_costo" | str | Centro de costos al que pertenece el costo. Valor fijo: "Agroquimico"
"subcategoria" | str | Subcategoría de agroquímico. Valores posibles: ["Fertilizante", "Fungicida", "Insectida", "Herbicida"]
"cultivo" | str | Cultivo al que se asocia el costo. Valores posibles: [Aseo y ornato, Campo General, Choclo, Frambuesas, Papas, Pasto, Peonías] o "N/A"
"proveedor" | str | Nombre del proveedor. Valor seleccionado de una hoja con una lista modificable de proveedores
"numero_folio" | str | Número de factura (es un valor numérico). Valores posibles: '1234567' o 'N/A'
"fecha_emision" | str | Fecha en que fue emitida la factura. Valores posibles: datetime(str) o 'N/A'. Nota: datetime transformado a str
"fecha_vencimiento_30" | str | Fecha de vencimiento a 30 días. Valores posibles: datetime(str), 'Por definir' o 'N/A'
"tipo_pago_30" | str | Tipo de pago para factura con vencimiento a 30 días. Valores posibles: ["Banco de Chile", "Banco Edwards", "Banco Bice", "Caja Chica", "Efectivo"] o 'N/A'
"fecha_vencimiento_60" | str | Fecha de vencimiento a 60 días. Valores posibles: datetime(str), 'Por definir' o 'N/A'
"tipo_pago_60" | str | Tipo de pago para factura con vencimiento a 60 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_90" | str | Fecha de vencimiento a 90 días. Valores posibles: datetime(str), 'Por definir' o 'N/A'
"tipo_pago_90" | str | Tipo de pago para factura con vencimiento a 90 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_120" | str | Fecha de vencimiento a 120 días. Valores posibles: datetime(str), 'Por definir' o 'N/A'
"tipo_pago_120" | str | Tipo de pago para factura con vencimiento a 120 días. Mismos valores que "tipo_pago_30"
"comentario" | str | Comentario opcional sobre el costo. Valores posibles: str o None

# Hoja "maquinaria"

Columna | Tipo | Definición
"id" | int | Id único
"fecha_envio_form" | str | Fecha en que el usuario guardó el formulario. Nota: datetime transformado a str. Ej: 'dd/mm/yyyy hh:mm:ss'
"descripcion" | str | Nota corta que describe el costo
"valor_bruto" | int | Valor del costo IVA incluido
"valor_neto" | int | Valor del costo sin IVA
"iva" | int | IVA del costo
"centro_costo" | str | Centro de costos al que pertenece el costo. Valor fijo: "Maquinaria"
"subcategoria" | str | Subcategoría de Maquinaria. Valores posibles: ["Mantenimiento", "Reparación", "Mejora", "Servicio a Terceros"]
"maquina" | str | Nombre de la máquina asociada. Valor seleccionado de una hoja con una lista modificable de máquinas
"proveedor" | str | Nombre del proveedor. Valor seleccionado de una hoja con una lista modificable de proveedores
"numero_folio" | str | Número de factura (es un valor numérico). Valores posibles: '1234567' o 'N/A'
"fecha_emision" | str | Fecha en que fue emitida la factura. Valores posibles: datetime(str) o 'N/A'. Nota: datetime transformado a str
"fecha_vencimiento_30" | str | Fecha de vencimiento a 30 días. Valores posibles: datetime(str), 'Por definir' o 'N/A'
"tipo_pago_30" | str | Tipo de pago para factura con vencimiento a 30 días. Valores posibles: ["Banco de Chile", "Banco Edwards", "Banco Bice", "Caja Chica", "Efectivo"] o 'N/A'
"fecha_vencimiento_60" | str | Fecha de vencimiento a 60 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_60" | str | Tipo de pago para factura con vencimiento a 60 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_90" | str | Fecha de vencimiento a 90 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_90" | str | Tipo de pago para factura con vencimiento a 90 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_120" | str | Fecha de vencimiento a 120 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_120" | str | Tipo de pago para factura con vencimiento a 120 días. Mismos valores que "tipo_pago_30"
"comentario" | str | Comentario opcional sobre el costo. Valores posibles: str o None

# Hoja "administracion"

Columna | Tipo | Definición
"id" | int | Id único
"fecha_envio_form" | str | Fecha en que el usuario guardó el formulario. Nota: datetime transformado a str. Ej: 'dd/mm/yyyy hh:mm:ss'
"descripcion" | str | Nota corta que describe el costo
"valor_bruto" | int | Valor del costo IVA incluido
"valor_neto" | int | Valor del costo sin IVA
"iva" | int | IVA del costo
"centro_costo" | str | Centro de costos al que pertenece el costo. Valor fijo: "Administracion"
"subcategoria" | str | Subcategoría de Administración. Valores posibles: ["Asesorias", "Subscripciones", "Viajes", "Form 29"]
"proveedor" | str | Nombre del proveedor. Valor seleccionado de una hoja con una lista modificable de proveedores
"numero_folio" | str | Número de factura (es un valor numérico). Valores posibles: '1234567' o 'N/A'
"fecha_emision" | str | Fecha en que fue emitida la factura. Valores posibles: datetime(str) o 'N/A'. Nota: datetime transformado a str
"fecha_vencimiento_30" | str | Fecha de vencimiento a 30 días. Valores posibles: datetime(str), 'Por definir' o 'N/A'
"tipo_pago_30" | str | Tipo de pago para factura con vencimiento a 30 días. Valores posibles: ["Banco de Chile", "Banco Edwards", "Banco Bice", "Caja Chica", "Efectivo"] o 'N/A'
"fecha_vencimiento_60" | str | Fecha de vencimiento a 60 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_60" | str | Tipo de pago para factura con vencimiento a 60 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_90" | str | Fecha de vencimiento a 90 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_90" | str | Tipo de pago para factura con vencimiento a 90 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_120" | str | Fecha de vencimiento a 120 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_120" | str | Tipo de pago para factura con vencimiento a 120 días. Mismos valores que "tipo_pago_30"
"comentario" | str | Comentario opcional sobre el costo. Valores posibles: str o None

# Hoja "seguros"

Columna | Tipo | Definición
"id" | int | Id único
"fecha_envio_form" | str | Fecha en que el usuario guardó el formulario. Nota: datetime transformado a str. Ej: 'dd/mm/yyyy hh:mm:ss'
"descripcion" | str | Nota corta que describe el costo
"valor_bruto" | int | Valor del costo IVA incluido
"valor_neto" | int | Valor del costo sin IVA
"iva" | int | IVA del costo
"centro_costo" | str | Centro de costos al que pertenece el costo. Valor fijo: "Seguros"
"subcategoria" | str | Subcategoría de Seguros. Valores posibles: ["Transporte", "Equipos", "Infraestructura", "Cultivos"]
"maquina" | str | Nombre de la máquina asegurada. Valor seleccionado de una hoja con una lista modificable de máquinas. Solo aplica si subcategoria = "Equipos", en otro caso 'N/A'
"cultivo" | str | Nombre del cultivo asegurado. Valores posibles: ["Aseo y ornato", "Campo General", "Choclo", "Frambuesas", "Papas", "Pasto", "Peonías"] o 'N/A'. Solo aplica si subcategoria = "Cultivos"
"transporte" | str | Tipo de transporte asegurado. Valores posibles: ["Importación", "Exportación", "Carga Nacional"] o 'N/A'. Solo aplica si subcategoria = "Transporte"
"proveedor" | str | Nombre del proveedor. Valor seleccionado de una hoja con una lista modificable de proveedores
"numero_folio" | str | Número de factura (valor numérico). Valores posibles: '1234567' o 'N/A'
"fecha_emision" | str | Fecha en que fue emitida la factura. Valores posibles: datetime(str) o 'N/A'
"fecha_vencimiento_30" | str | Fecha de vencimiento a 30 días. Valores posibles: datetime(str), 'Por definir' o 'N/A'
"tipo_pago_30" | str | Tipo de pago para factura con vencimiento a 30 días. Valores posibles: ["Banco de Chile", "Banco Edwards", "Banco Bice", "Caja Chica", "Efectivo"] o 'N/A'
"fecha_vencimiento_60" | str | Fecha de vencimiento a 60 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_60" | str | Tipo de pago para factura con vencimiento a 60 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_90" | str | Fecha de vencimiento a 90 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_90" | str | Tipo de pago para factura con vencimiento a 90 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_120" | str | Fecha de vencimiento a 120 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_120" | str | Tipo de pago para factura con vencimiento a 120 días. Mismos valores que "tipo_pago_30"
"comentario" | str | Comentario opcional sobre el costo. Valores posibles: str o None

# Hoja "inversiones"

Columna | Tipo | Definición
"id" | int | Id único
"fecha_envio_form" | str | Fecha en que el usuario guardó el formulario. Nota: datetime transformado a str. Ej: 'dd/mm/yyyy hh:mm:ss'
"descripcion" | str | Nota corta que describe el costo
"valor_bruto" | int | Valor del costo IVA incluido
"valor_neto" | int | Valor del costo sin IVA
"iva" | int | IVA del costo
"centro_costo" | str | Centro de costos al que pertenece el costo. Valor fijo: "Inversiones"
"subcategoria" | str | Subcategoría de la inversión. Valores posibles: ["Maquinaria", "Infraestructura", "Equipos", "Preparación Previa"]
"cultivo" | str | Nombre del cultivo vinculado a la inversión (si aplica). Valores posibles: ["Aseo y ornato", "Campo General", "Choclo", "Frambuesas", "Papas", "Pasto", "Peonías"] o 'N/A'
"preparacion_previa" | str | Solo aplica si "subcategoria" = "Preparación Previa". Valores posibles: ["Preparación de Suelo", "Agroquímico"] o 'N/A'
"proveedor" | str | Nombre del proveedor. Valor seleccionado de una hoja con una lista modificable de proveedores
"numero_folio" | str | Número de factura (valor numérico). Valores posibles: '1234567' o 'N/A'
"fecha_emision" | str | Fecha en que fue emitida la factura. Valores posibles: datetime(str) o 'N/A'
"fecha_vencimiento_30" | str | Fecha de vencimiento a 30 días. Valores posibles: datetime(str), 'Por definir' o 'N/A'
"tipo_pago_30" | str | Tipo de pago para factura con vencimiento a 30 días. Valores posibles: ["Banco de Chile", "Banco Edwards", "Banco Bice", "Caja Chica", "Efectivo"] o 'N/A'
"fecha_vencimiento_60" | str | Fecha de vencimiento a 60 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_60" | str | Tipo de pago para factura con vencimiento a 60 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_90" | str | Fecha de vencimiento a 90 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_90" | str | Tipo de pago para factura con vencimiento a 90 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_120" | str | Fecha de vencimiento a 120 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_120" | str | Tipo de pago para factura con vencimiento a 120 días. Mismos valores que "tipo_pago_30"
"comentario" | str | Comentario opcional sobre el costo. Valores posibles: str o None

# Hoja "servicios_externos"

Columna | Tipo | Definición
"id" | int | Id único
"fecha_envio_form" | str | Fecha en que el usuario guardó el formulario. Nota: datetime transformado a str. Ej: 'dd/mm/yyyy hh:mm:ss'
"descripcion" | str | Nota corta que describe el costo
"valor_bruto" | int | Valor del costo IVA incluido
"valor_neto" | int | Valor del costo sin IVA
"iva" | int | IVA del costo
"centro_costo" | str | Centro de costos al que pertenece el costo. Valor fijo: "Servicio Externos MMOO"
"subcategoria" | str | Tipo de servicio externo contratado. Valores posibles: ["Cosecha", "Selección", "Plantación", "Limpieza", "Aseo y ornato", "Otros"]
"cultivo" | str | Cultivo vinculado al servicio. Valores posibles: ["Aseo y ornato", "Campo General", "Choclo", "Frambuesas", "Papas", "Pasto", "Peonías"] o 'N/A'
"proveedor" | str | Nombre del proveedor. Valor seleccionado de una hoja con una lista modificable de proveedores
"numero_folio" | str | Número de factura (valor numérico). Valores posibles: '1234567' o 'N/A'
"fecha_emision" | str | Fecha en que fue emitida la factura. Valores posibles: datetime(str) o 'N/A'
"fecha_vencimiento_30" | str | Fecha de vencimiento a 30 días. Valores posibles: datetime(str), 'Por definir' o 'N/A'
"tipo_pago_30" | str | Tipo de pago para factura con vencimiento a 30 días. Valores posibles: ["Banco de Chile", "Banco Edwards", "Banco Bice", "Caja Chica", "Efectivo"] o 'N/A'
"fecha_vencimiento_60" | str | Fecha de vencimiento a 60 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_60" | str | Tipo de pago para factura con vencimiento a 60 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_90" | str | Fecha de vencimiento a 90 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_90" | str | Tipo de pago para factura con vencimiento a 90 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_120" | str | Fecha de vencimiento a 120 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_120" | str | Tipo de pago para factura con vencimiento a 120 días. Mismos valores que "tipo_pago_30"
"comentario" | str | Comentario opcional sobre el costo. Valores posibles: str o None

# Hoja "servicios_basicos"

Columna | Tipo | Definición
"id" | int | Id único
"fecha_envio_form" | str | Fecha en que el usuario guardó el formulario. Nota: datetime transformado a str. Ej: 'dd/mm/yyyy hh:mm:ss'
"descripcion" | str | Nota corta que describe el costo
"valor_bruto" | int | Valor del costo IVA incluido
"valor_neto" | int | Valor del costo sin IVA
"iva" | int | IVA del costo
"centro_costo" | str | Centro de costos al que pertenece el costo. Valor fijo: "Servicios Básicos"
"subcategoria" | str | Tipo de servicio básico. Valores posibles: ["Agua", "Luz", "Gas", "Luz2 (Riego)"]
"proveedor" | str | Nombre del proveedor. Valor seleccionado de una hoja con una lista modificable de proveedores
"numero_folio" | str | Número de factura (valor numérico). Valores posibles: '1234567' o 'N/A'
"fecha_emision" | str | Fecha en que fue emitida la factura. Valores posibles: datetime(str) o 'N/A'
"fecha_vencimiento_30" | str | Fecha de vencimiento a 30 días. Valores posibles: datetime(str), 'Por definir' o 'N/A'
"tipo_pago_30" | str | Tipo de pago para factura con vencimiento a 30 días. Valores posibles: ["Banco de Chile", "Banco Edwards", "Banco Bice", "Caja Chica", "Efectivo"] o 'N/A'
"fecha_vencimiento_60" | str | Fecha de vencimiento a 60 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_60" | str | Tipo de pago para factura con vencimiento a 60 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_90" | str | Fecha de vencimiento a 90 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_90" | str | Tipo de pago para factura con vencimiento a 90 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_120" | str | Fecha de vencimiento a 120 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_120" | str | Tipo de pago para factura con vencimiento a 120 días. Mismos valores que "tipo_pago_30"
"comentario" | str | Comentario opcional sobre el costo. Valores posibles: str o None

# Hoja "combustibles"

Columna | Tipo | Definición
"id" | int | Id único
"fecha_envio_form" | str | Fecha en que el usuario guardó el formulario. Nota: datetime transformado a str. Ej: 'dd/mm/yyyy hh:mm:ss'
"descripcion" | str | Nota corta que describe el costo
"valor_bruto" | int | Valor del costo IVA incluido
"valor_neto" | int | Valor del costo sin IVA
"iva" | int | IVA del costo
"centro_costo" | str | Centro de costos al que pertenece el costo. Valor fijo: "Combustibles"
"subcategoria" | str | Tipo de combustible. Valores posibles: ["Petróleo", "Bencina", "Energia"]
"proveedor" | str | Nombre del proveedor. Valor seleccionado de una hoja con una lista modificable de proveedores
"numero_folio" | str | Número de factura (valor numérico). Valores posibles: '1234567' o 'N/A'
"fecha_emision" | str | Fecha en que fue emitida la factura. Valores posibles: datetime(str) o 'N/A'
"fecha_vencimiento_30" | str | Fecha de vencimiento a 30 días. Valores posibles: datetime(str), 'Por definir' o 'N/A'
"tipo_pago_30" | str | Tipo de pago para factura con vencimiento a 30 días. Valores posibles: ["Banco de Chile", "Banco Edwards", "Banco Bice", "Caja Chica", "Efectivo"] o 'N/A'
"fecha_vencimiento_60" | str | Fecha de vencimiento a 60 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_60" | str | Tipo de pago para factura con vencimiento a 60 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_90" | str | Fecha de vencimiento a 90 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_90" | str | Tipo de pago para factura con vencimiento a 90 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_120" | str | Fecha de vencimiento a 120 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_120" | str | Tipo de pago para factura con vencimiento a 120 días. Mismos valores que "tipo_pago_30"
"comentario" | str | Comentario opcional sobre el costo. Valores posibles: str o None

# Hoja "gastos_varios"

Columna | Tipo | Definición
"id" | int | Id único
"fecha_envio_form" | str | Fecha en que el usuario guardó el formulario. Nota: datetime transformado a str. Ej: 'dd/mm/yyyy hh:mm:ss'
"descripcion" | str | Nota corta que describe el costo
"valor_bruto" | int | Valor del costo IVA incluido
"valor_neto" | int | Valor del costo sin IVA
"iva" | int | IVA del costo
"centro_costo" | str | Centro de costos al que pertenece el costo. Valor fijo: "Gastos Varios / Otros"
"proveedor" | str | Nombre del proveedor. Valor seleccionado de una hoja con una lista modificable de proveedores
"numero_folio" | str | Número de factura (valor numérico). Valores posibles: '1234567' o 'N/A'
"fecha_emision" | str | Fecha en que fue emitida la factura. Valores posibles: datetime(str) o 'N/A'
"fecha_vencimiento_30" | str | Fecha de vencimiento a 30 días. Valores posibles: datetime(str), 'Por definir' o 'N/A'
"tipo_pago_30" | str | Tipo de pago para factura con vencimiento a 30 días. Valores posibles: ["Banco de Chile", "Banco Edwards", "Banco Bice", "Caja Chica", "Efectivo"] o 'N/A'
"fecha_vencimiento_60" | str | Fecha de vencimiento a 60 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_60" | str | Tipo de pago para factura con vencimiento a 60 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_90" | str | Fecha de vencimiento a 90 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_90" | str | Tipo de pago para factura con vencimiento a 90 días. Mismos valores que "tipo_pago_30"
"fecha_vencimiento_120" | str | Fecha de vencimiento a 120 días. Mismos valores que "fecha_vencimiento_30"
"tipo_pago_120" | str | Tipo de pago para factura con vencimiento a 120 días. Mismos valores que "tipo_pago_30"
"comentario" | str | Comentario opcional sobre el costo. Valores posibles: str o None

# Hoja "ingresos"

| **Columna**                | **Tipo** | **Definición** |
|----------------------------|----------|----------------|
| `id`                       | int      | Id único incremental por fila. Se calcula según el largo actual de la hoja. |
| `fecha_envio`              | str      | Fecha y hora en que el usuario guardó el formulario. Formato string: `'dd/mm/yyyy hh:mm:ss'`. |
| `descripcion`              | str      | Descripción breve del ingreso registrado. Ejemplo: `"Venta de papas a cliente X"`. |
| `valor_bruto`              | int      | Valor total del ingreso incluyendo IVA. |
| `valor_neto`               | int      | Valor del ingreso sin IVA. Calculado automáticamente como `valor_bruto - iva`. |
| `iva`                      | int      | IVA correspondiente al ingreso (por defecto 19% del valor bruto). |
| `cultivo`                  | str      | Cultivo asociado al ingreso. Ejemplos: `["Choclo", "Frambuesas", "Papas", "Pasto", "Peonías"]`. |
| `cliente`                  | str      | Nombre del cliente asociado al ingreso. |
| `numero_folio`             | str      | Número de folio de la factura asociada. Puede ser numérico como string (`'1234567'`) o `'N/A'` si no aplica. |
| `fecha_ingreso`            | str      | Fecha en que fue recibido el ingreso o emitida la factura. Formato string `'dd/mm/yyyy'`. |
| `fecha_vencimiento_30`     | str      | Fecha de vencimiento a 30 días. Valores posibles: `'dd/mm/yyyy'`, `'Por definir'` o `'N/A'`. |
| `tipo_pago_30`             | str      | Tipo de pago correspondiente al vencimiento a 30 días. Valores posibles: `["Banco de Chile", "Banco Edwards", "Banco Bice", "Caja Chica", "Efectivo"]` o `'N/A'`. |
| `fecha_vencimiento_60`     | str      | Igual que `fecha_vencimiento_30`, pero a 60 días. |
| `tipo_pago_60`             | str      | Igual que `tipo_pago_30`, pero para el vencimiento a 60 días. |
| `fecha_vencimiento_90`     | str      | Igual que `fecha_vencimiento_30`, pero a 90 días. |
| `tipo_pago_90`             | str      | Igual que `tipo_pago_30`, pero para el vencimiento a 90 días. |
| `fecha_vencimiento_120`    | str      | Igual que `fecha_vencimiento_30`, pero a 120 días. |
| `tipo_pago_120`            | str      | Igual que `tipo_pago_30`, pero para el vencimiento a 120 días. |
| `comentarios`              | str      | Comentario opcional sobre el ingreso. Puede ser un texto libre o `None`. |