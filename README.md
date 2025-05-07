# WIP

TODO: 
* Traducir al inglés
* Agregar si columna acepta o no "null"

Hojas: ["rrhh"(WIP), "agroquimicos", "maquinaria", "administracion", "seguros", "inversiones", "servicios_externos", "servicios_basicos", "combustibles", "gastos_varios"]

# Notes:
## Leyes Sociales para sueldos

| **Ítem**                            | **% Aproximado** | **Responsable** | **Descripción**                                                            | **Ejemplo (sueldo bruto \$1.000.000)** |
| ----------------------------------- | ---------------- | --------------- | -------------------------------------------------------------------------- | -------------------------------------- |
| **Sueldo Bruto**                    | -                | -               | Remuneración total antes de descuentos                                     | \$1.000.000                            |
| **AFP (previsión)**                 | 10% + comisión   | Trabajador      | Fondo de pensiones obligatorio                                             | \$100.000 + comisión (ej. \$11.000)    |
| **Salud (Fonasa o Isapre)**         | 7%               | Trabajador      | Cobertura de salud pública o privada                                       | \$70.000                               |
| **Seguro de Cesantía**              | 0.6%             | Trabajador      | Protección ante desempleo (solo indefinidos)                               | \$6.000                                |
| **Seguro de Cesantía**              | 2.4%             | Empleador       | Aporte adicional del empleador                                             | \$24.000                               |
| **SIS (invalidez y sobrevivencia)** | 1.53%            | Empleador       | Seguro obligatorio de la AFP, cubre invalidez o fallecimiento              | \$15.300                               |
| **ATEP (accidentes laborales)**     | 0.93% – 3.4%     | Empleador       | Seguro por accidentes del trabajo o trayecto, varía según riesgo del rubro | \$9.300 (mínimo legal)                 |
| **Impuesto Único (si aplica)**      | Variable         | Trabajador      | Según tabla SII, si el sueldo supera los tramos exentos                    | \$0 – depende del sueldo               |
| **Sueldo Líquido Aproximado**       | -                | -               | Total a pagar al trabajador tras descuentos legales                        | \~\$813.000                            |


# Data Dictionary

## Hoja "rrhh"

| **Columna**             | **Tipo** | **Definición**                                                                         |
| ----------------------- | -------- | -------------------------------------------------------------------------------------- |
| `id`                    | int      | Id único incremental por fila.                                                         |
| `fecha_envio_form`      | str      | Fecha y hora en que el usuario guardó el formulario. Formato: `'dd/mm/yyyy hh:mm:ss'`. |
| `descripcion`           | str      | Nota corta que describe el costo.                                                      |
| `valor_bruto`           | int      | Valor del costo IVA incluido.                                                          |
| `valor_neto`            | int      | Valor del costo sin IVA.                                                               |
| `iva`                   | int      | IVA del costo.                                                                         |
| `centro_costo`          | str      | Centro de costos. Valor fijo: `"RRHH"`.                                                |
| `subcategoria`          | str      | Subcategoría de RRHH. Ej: `["Sueldo administrativo", "Bonos", "Viáticos", etc.]`.      |
| `cultivo`               | str      | Cultivo asociado. Ej: `["Choclo", "Frambuesas", "Papas", "N/A"]`.                      |
| `numero_folio`          | str      | Número de factura. Ej: `'1234567'` o `'N/A'`.                                          |
| `fecha_emision`         | str      | Fecha de emisión de la factura. Ej: `'dd/mm/yyyy'` o `'N/A'`.                          |
| `fecha_vencimiento_30`  | str      | Fecha de vencimiento a 30 días. Ej: `'dd/mm/yyyy'`, `'Por definir'`, `'N/A'`.          |
| `tipo_pago_30`          | str      | Tipo de pago a 30 días. Ej: `"Banco de Chile"` o `'N/A'`.                              |
| `fecha_vencimiento_60`  | str      | Igual que `fecha_vencimiento_30`.                                                      |
| `tipo_pago_60`          | str      | Igual que `tipo_pago_30`.                                                              |
| `fecha_vencimiento_90`  | str      | Igual que `fecha_vencimiento_30`.                                                      |
| `tipo_pago_90`          | str      | Igual que `tipo_pago_30`.                                                              |
| `fecha_vencimiento_120` | str      | Igual que `fecha_vencimiento_30`.                                                      |
| `tipo_pago_120`         | str      | Igual que `tipo_pago_30`.                                                              |
| `comentario`            | str      | Comentario opcional. Texto libre o `None`.                                             |

## Hoja "agroquimicos"

| **Columna**             | **Tipo** | **Definición**                                                                         |
| ----------------------- | -------- | -------------------------------------------------------------------------------------- |
| `id`                    | int      | Id único incremental por fila.                                                         |
| `fecha_envio_form`      | str      | Fecha y hora en que el usuario guardó el formulario. Formato: `'dd/mm/yyyy hh:mm:ss'`. |
| `descripcion`           | str      | Nota corta que describe el costo.                                                      |
| `valor_bruto`           | int      | Valor del costo IVA incluido.                                                          |
| `valor_neto`            | int      | Valor del costo sin IVA.                                                               |
| `iva`                   | int      | IVA del costo.                                                                         |
| `centro_costo`          | str      | Centro de costos. Valor fijo: "Agroquimico".                                           |
| `subcategoria`          | str      | Tipo de agroquímico. Ej: `["Fertilizante", "Fungicida", "Insectida", "Herbicida"]`.    |
| `cultivo`               | str      | Cultivo asociado. Ej: `["Choclo", "Frambuesas", "Papas", "N/A"]`.                      |
| `proveedor`             | str      | Nombre del proveedor. Seleccionado desde hoja auxiliar.                                |
| `numero_folio`          | str      | Número de factura. Ej: `'1234567'` o `'N/A'`.                                          |
| `fecha_emision`         | str      | Fecha de emisión. Ej: `'dd/mm/yyyy'` o `'N/A'`.                                        |
| `fecha_vencimiento_30`  | str      | Fecha de vencimiento a 30 días.                                                        |
| `tipo_pago_30`          | str      | Tipo de pago a 30 días. Ej: `'Banco de Chile'`, `'Caja Chica'`, `'N/A'`.               |
| `fecha_vencimiento_60`  | str      | Igual que `fecha_vencimiento_30`.                                                      |
| `tipo_pago_60`          | str      | Igual que `tipo_pago_30`.                                                              |
| `fecha_vencimiento_90`  | str      | Igual que `fecha_vencimiento_30`.                                                      |
| `tipo_pago_90`          | str      | Igual que `tipo_pago_30`.                                                              |
| `fecha_vencimiento_120` | str      | Igual que `fecha_vencimiento_30`.                                                      |
| `tipo_pago_120`         | str      | Igual que `tipo_pago_30`.                                                              |
| `comentario`            | str      | Comentario opcional. Texto libre o `None`.                                             |

## Hoja "maquinaria"

| **Columna**             | **Tipo** | **Definición**                                                          |
| ----------------------- | -------- | ----------------------------------------------------------------------- |
| `id`                    | int      | Id único incremental.                                                   |
| `fecha_envio_form`      | str      | Fecha y hora de envío. `'dd/mm/yyyy hh:mm:ss'`.                         |
| `descripcion`           | str      | Nota corta que describe el costo.                                       |
| `valor_bruto`           | int      | Valor con IVA.                                                          |
| `valor_neto`            | int      | Valor sin IVA.                                                          |
| `iva`                   | int      | IVA correspondiente.                                                    |
| `centro_costo`          | str      | Valor fijo: `"Maquinaria"`.                                             |
| `subcategoria`          | str      | Ej: `["Mantenimiento", "Reparación", "Mejora", "Servicio a Terceros"]`. |
| `maquina`               | str      | Máquina seleccionada desde lista auxiliar.                              |
| `proveedor`             | str      | Proveedor desde hoja auxiliar.                                          |
| `numero_folio`          | str      | `'1234567'` o `'N/A'`.                                                  |
| `fecha_emision`         | str      | Fecha emisión o `'N/A'`.                                                |
| `fecha_vencimiento_30`  | str      | `'dd/mm/yyyy'`, `'Por definir'`, `'N/A'`.                               |
| `tipo_pago_30`          | str      | Tipo de pago a 30 días.                                                 |
| `fecha_vencimiento_60`  | str      | Igual que `fecha_vencimiento_30`.                                       |
| `tipo_pago_60`          | str      | Igual que `tipo_pago_30`.                                               |
| `fecha_vencimiento_90`  | str      | Igual que `fecha_vencimiento_30`.                                       |
| `tipo_pago_90`          | str      | Igual que `tipo_pago_30`.                                               |
| `fecha_vencimiento_120` | str      | Igual que `fecha_vencimiento_30`.                                       |
| `tipo_pago_120`         | str      | Igual que `tipo_pago_30`.                                               |
| `comentario`            | str      | Comentario opcional o `None`.                                           |

## Hoja "administracion"

| **Columna**             | **Tipo** | **Definición**                                              |
| ----------------------- | -------- | ----------------------------------------------------------- |
| `id`                    | int      | Id único.                                                   |
| `fecha_envio_form`      | str      | Fecha y hora del envío.                                     |
| `descripcion`           | str      | Descripción del gasto.                                      |
| `valor_bruto`           | int      | Total con IVA.                                              |
| `valor_neto`            | int      | Valor sin IVA.                                              |
| `iva`                   | int      | Monto de IVA.                                               |
| `centro_costo`          | str      | Valor fijo: `"Administracion"`.                             |
| `subcategoria`          | str      | Ej: `["Asesorias", "Subscripciones", "Viajes", "Form 29"]`. |
| `proveedor`             | str      | Desde hoja de proveedores.                                  |
| `numero_folio`          | str      | `'1234567'` o `'N/A'`.                                      |
| `fecha_emision`         | str      | Fecha o `'N/A'`.                                            |
| `fecha_vencimiento_30`  | str      | `'dd/mm/yyyy'`, `'Por definir'`, `'N/A'`.                   |
| `tipo_pago_30`          | str      | Modo de pago.                                               |
| `fecha_vencimiento_60`  | str      | Igual que 30 días.                                          |
| `tipo_pago_60`          | str      | Igual que tipo\_pago\_30.                                   |
| `fecha_vencimiento_90`  | str      | Igual que 30 días.                                          |
| `tipo_pago_90`          | str      | Igual que tipo\_pago\_30.                                   |
| `fecha_vencimiento_120` | str      | Igual que 30 días.                                          |
| `tipo_pago_120`         | str      | Igual que tipo\_pago\_30.                                   |
| `comentario`            | str      | Opcional o `None`.                                          |


## Hoja "seguros"

| **Columna**             | **Tipo** | **Definición**                                                                            |
| ----------------------- | -------- | ----------------------------------------------------------------------------------------- |
| `id`                    | int      | Id único incremental por fila.                                                            |
| `fecha_envio_form`      | str      | Fecha y hora en que el usuario guardó el formulario. Formato `'dd/mm/yyyy hh:mm:ss'`.     |
| `descripcion`           | str      | Nota corta que describe el costo.                                                         |
| `valor_bruto`           | int      | Valor del costo IVA incluido.                                                             |
| `valor_neto`            | int      | Valor del costo sin IVA.                                                                  |
| `iva`                   | int      | IVA del costo.                                                                            |
| `centro_costo`          | str      | Centro de costos al que pertenece el costo. Valor fijo: `"Seguros"`.                      |
| `subcategoria`          | str      | Subcategoría del seguro. Ej.: `["Transporte", "Equipos", "Infraestructura", "Cultivos"]`. |
| `maquina`               | str      | Máquina asegurada. Solo aplica si `subcategoria = "Equipos"`. Si no, usar `'N/A'`.        |
| `cultivo`               | str      | Cultivo asegurado. Solo aplica si `subcategoria = "Cultivos"`.                            |
| `transporte`            | str      | Tipo de transporte asegurado. Solo aplica si `subcategoria = "Transporte"`.               |
| `proveedor`             | str      | Nombre del proveedor. Seleccionado desde lista.                                           |
| `numero_folio`          | str      | Número de factura como string. Ej.: `'1234567'` o `'N/A'`.                                |
| `fecha_emision`         | str      | Fecha de emisión de la factura.                                                           |
| `fecha_vencimiento_30`  | str      | Fecha de vencimiento a 30 días.                                                           |
| `tipo_pago_30`          | str      | Tipo de pago a 30 días.                                                                   |
| `fecha_vencimiento_60`  | str      | Fecha de vencimiento a 60 días.                                                           |
| `tipo_pago_60`          | str      | Tipo de pago a 60 días.                                                                   |
| `fecha_vencimiento_90`  | str      | Fecha de vencimiento a 90 días.                                                           |
| `tipo_pago_90`          | str      | Tipo de pago a 90 días.                                                                   |
| `fecha_vencimiento_120` | str      | Fecha de vencimiento a 120 días.                                                          |
| `tipo_pago_120`         | str      | Tipo de pago a 120 días.                                                                  |
| `comentario`            | str      | Comentario opcional. Texto libre o `None`.                                                |


## Hoja "inversiones"

| **Columna**             | **Tipo** | **Definición**                                                                                        |
| ----------------------- | -------- | ----------------------------------------------------------------------------------------------------- |
| `id`                    | int      | Id único incremental por fila.                                                                        |
| `fecha_envio_form`      | str      | Fecha y hora en que el usuario guardó el formulario.                                                  |
| `descripcion`           | str      | Descripción breve del gasto.                                                                          |
| `valor_bruto`           | int      | Valor total del gasto, IVA incluido.                                                                  |
| `valor_neto`            | int      | Valor sin IVA.                                                                                        |
| `iva`                   | int      | IVA correspondiente al gasto.                                                                         |
| `centro_costo`          | str      | Centro de costos. Valor fijo: `"Inversiones"`.                                                        |
| `subcategoria`          | str      | Subcategoría de inversión. Ej.: `["Maquinaria", "Infraestructura", "Equipos", "Preparación Previa"]`. |
| `cultivo`               | str      | Cultivo asociado o `'N/A'`.                                                                           |
| `preparacion_previa`    | str      | Aplica solo si `subcategoria = "Preparación Previa"`. Ej.: `["Preparación de Suelo", "Agroquímico"]`. |
| `proveedor`             | str      | Nombre del proveedor.                                                                                 |
| `numero_folio`          | str      | Número de factura.                                                                                    |
| `fecha_emision`         | str      | Fecha de emisión.                                                                                     |
| `fecha_vencimiento_30`  | str      | Fecha de vencimiento a 30 días.                                                                       |
| `tipo_pago_30`          | str      | Tipo de pago a 30 días.                                                                               |
| `fecha_vencimiento_60`  | str      | Fecha de vencimiento a 60 días.                                                                       |
| `tipo_pago_60`          | str      | Tipo de pago a 60 días.                                                                               |
| `fecha_vencimiento_90`  | str      | Fecha de vencimiento a 90 días.                                                                       |
| `tipo_pago_90`          | str      | Tipo de pago a 90 días.                                                                               |
| `fecha_vencimiento_120` | str      | Fecha de vencimiento a 120 días.                                                                      |
| `tipo_pago_120`         | str      | Tipo de pago a 120 días.                                                                              |
| `comentario`            | str      | Comentario opcional.                                                                                  |


## Hoja "servicios_externos"

| **Columna**             | **Tipo** | **Definición**                                                                                         |
| ----------------------- | -------- | ------------------------------------------------------------------------------------------------------ |
| `id`                    | int      | Id único incremental por fila.                                                                         |
| `fecha_envio_form`      | str      | Fecha y hora en que el usuario guardó el formulario. Formato `'dd/mm/yyyy hh:mm:ss'`.                  |
| `descripcion`           | str      | Descripción del servicio externo contratado.                                                           |
| `valor_bruto`           | int      | Valor total del costo, IVA incluido.                                                                   |
| `valor_neto`            | int      | Valor sin IVA.                                                                                         |
| `iva`                   | int      | IVA correspondiente al costo.                                                                          |
| `centro_costo`          | str      | Centro de costos. Valor fijo: `"Servicio Externos MMOO"`.                                              |
| `subcategoria`          | str      | Tipo de servicio. Ej.: `["Cosecha", "Selección", "Plantación", "Limpieza", "Aseo y ornato", "Otros"]`. |
| `cultivo`               | str      | Cultivo asociado o `'N/A'`.                                                                            |
| `proveedor`             | str      | Nombre del proveedor.                                                                                  |
| `numero_folio`          | str      | Número de factura como string.                                                                         |
| `fecha_emision`         | str      | Fecha de emisión.                                                                                      |
| `fecha_vencimiento_30`  | str      | Vencimiento a 30 días.                                                                                 |
| `tipo_pago_30`          | str      | Tipo de pago a 30 días.                                                                                |
| `fecha_vencimiento_60`  | str      | Vencimiento a 60 días.                                                                                 |
| `tipo_pago_60`          | str      | Tipo de pago a 60 días.                                                                                |
| `fecha_vencimiento_90`  | str      | Vencimiento a 90 días.                                                                                 |
| `tipo_pago_90`          | str      | Tipo de pago a 90 días.                                                                                |
| `fecha_vencimiento_120` | str      | Vencimiento a 120 días.                                                                                |
| `tipo_pago_120`         | str      | Tipo de pago a 120 días.                                                                               |
| `comentario`            | str      | Comentario opcional. Texto libre o `None`.                                                             |


## Hoja "servicios_basicos"

| **Columna**             | **Tipo** | **Definición**                                                   |
| ----------------------- | -------- | ---------------------------------------------------------------- |
| `id`                    | int      | Id único incremental por fila.                                   |
| `fecha_envio_form`      | str      | Fecha y hora de envío del formulario.                            |
| `descripcion`           | str      | Descripción del servicio básico.                                 |
| `valor_bruto`           | int      | Valor total con IVA.                                             |
| `valor_neto`            | int      | Valor sin IVA.                                                   |
| `iva`                   | int      | IVA del costo.                                                   |
| `centro_costo`          | str      | Centro de costos. Valor fijo: `"Servicios Básicos"`.             |
| `subcategoria`          | str      | Tipo de servicio. Ej.: `["Agua", "Luz", "Gas", "Luz2 (Riego)"]`. |
| `proveedor`             | str      | Nombre del proveedor.                                            |
| `numero_folio`          | str      | Número de factura.                                               |
| `fecha_emision`         | str      | Fecha de emisión.                                                |
| `fecha_vencimiento_30`  | str      | Vencimiento a 30 días.                                           |
| `tipo_pago_30`          | str      | Tipo de pago a 30 días.                                          |
| `fecha_vencimiento_60`  | str      | Vencimiento a 60 días.                                           |
| `tipo_pago_60`          | str      | Tipo de pago a 60 días.                                          |
| `fecha_vencimiento_90`  | str      | Vencimiento a 90 días.                                           |
| `tipo_pago_90`          | str      | Tipo de pago a 90 días.                                          |
| `fecha_vencimiento_120` | str      | Vencimiento a 120 días.                                          |
| `tipo_pago_120`         | str      | Tipo de pago a 120 días.                                         |
| `comentario`            | str      | Comentario opcional.                                             |


## Hoja "combustibles"

| **Columna**             | **Tipo** | **Definición**                                                  |
| ----------------------- | -------- | --------------------------------------------------------------- |
| `id`                    | int      | Id único incremental.                                           |
| `fecha_envio_form`      | str      | Fecha de envío del formulario.                                  |
| `descripcion`           | str      | Descripción del combustible.                                    |
| `valor_bruto`           | int      | Valor con IVA.                                                  |
| `valor_neto`            | int      | Valor sin IVA.                                                  |
| `iva`                   | int      | IVA correspondiente.                                            |
| `centro_costo`          | str      | Centro de costos. Valor fijo: `"Combustibles"`.                 |
| `subcategoria`          | str      | Tipo de combustible. Ej.: `["Petróleo", "Bencina", "Energia"]`. |
| `proveedor`             | str      | Nombre del proveedor.                                           |
| `numero_folio`          | str      | Número de factura.                                              |
| `fecha_emision`         | str      | Fecha de emisión.                                               |
| `fecha_vencimiento_30`  | str      | Vencimiento a 30 días.                                          |
| `tipo_pago_30`          | str      | Tipo de pago a 30 días.                                         |
| `fecha_vencimiento_60`  | str      | Vencimiento a 60 días.                                          |
| `tipo_pago_60`          | str      | Tipo de pago a 60 días.                                         |
| `fecha_vencimiento_90`  | str      | Vencimiento a 90 días.                                          |
| `tipo_pago_90`          | str      | Tipo de pago a 90 días.                                         |
| `fecha_vencimiento_120` | str      | Vencimiento a 120 días.                                         |
| `tipo_pago_120`         | str      | Tipo de pago a 120 días.                                        |
| `comentario`            | str      | Comentario opcional.                                            |

## Hoja "gastos_varios"

| **Columna**             | **Tipo** | **Definición**                                           |
| ----------------------- | -------- | -------------------------------------------------------- |
| `id`                    | int      | Id único.                                                |
| `fecha_envio_form`      | str      | Fecha de envío del formulario.                           |
| `descripcion`           | str      | Descripción breve del gasto.                             |
| `valor_bruto`           | int      | Valor con IVA.                                           |
| `valor_neto`            | int      | Valor sin IVA.                                           |
| `iva`                   | int      | IVA del gasto.                                           |
| `centro_costo`          | str      | Centro de costos. Valor fijo: `"Gastos Varios / Otros"`. |
| `proveedor`             | str      | Nombre del proveedor.                                    |
| `numero_folio`          | str      | Número de factura.                                       |
| `fecha_emision`         | str      | Fecha de emisión.                                        |
| `fecha_vencimiento_30`  | str      | Vencimiento a 30 días.                                   |
| `tipo_pago_30`          | str      | Tipo de pago a 30 días.                                  |
| `fecha_vencimiento_60`  | str      | Vencimiento a 60 días.                                   |
| `tipo_pago_60`          | str      | Tipo de pago a 60 días.                                  |
| `fecha_vencimiento_90`  | str      | Vencimiento a 90 días.                                   |
| `tipo_pago_90`          | str      | Tipo de pago a 90 días.                                  |
| `fecha_vencimiento_120` | str      | Vencimiento a 120 días.                                  |
| `tipo_pago_120`         | str      | Tipo de pago a 120 días.                                 |
| `comentario`            | str      | Comentario opcional.                                     |


## Hoja "ingresos"

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