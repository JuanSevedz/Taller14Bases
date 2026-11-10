# Punto 4. Arquitectura de la aplicación final

## 4.1. Diagrama de capas

```text
┌─────────────────────────────────────────────┐
│ NAVEGADOR WEB                               │
│ HTML + CSS                                  │
│ Muestra pantallas y envía solicitudes HTTP  │
└──────────────────────┬──────────────────────┘
                       ▼
┌─────────────────────────────────────────────┐
│ SERVIDOR WEB                                │
│ Python + Flask                              │
│ Recibe peticiones y selecciona las rutas    │
└──────────────────────┬──────────────────────┘
                       ▼
┌─────────────────────────────────────────────┐
│ CAPA DE DATOS                               │
│ Python: datos.py                            │
│ Centraliza consultas SQL y conexiones       │
└──────────────────────┬──────────────────────┘
                       ▼
┌─────────────────────────────────────────────┐
│ LIBRERÍA Y CONTROLADOR                      │
│ pyodbc → ODBC → psqlODBC (PostgreSQL Unicode)│
└──────────────────────┬──────────────────────┘
                       ▼
┌─────────────────────────────────────────────┐
│ BASE DE DATOS                               │
│ PostgreSQL alojado en Neon                  │
└─────────────────────────────────────────────┘
```

El navegador no se conecta directamente a PostgreSQL. Las peticiones llegan a Flask; Flask invoca
funciones de `datos.py`; este módulo utiliza `pyodbc` y psqlODBC para consultar Neon.

## 4.2. Configuración y protección de credenciales

La cadena ODBC se almacena en la variable de entorno `BD_ODBC`, definida localmente en `.env`.
Flask carga la configuración en el servidor mediante `python-dotenv`. El archivo `.env` se excluye
del repositorio mediante `.gitignore` y no se incluye en el ZIP ni en el informe.

Se entrega únicamente `.env.ejemplo`, con marcadores como `TU_SERVIDOR` y `TU_CONTRASENA`.
La contraseña permanece en el entorno del servidor y nunca se envía al navegador.

## 4.3. Funciones de la capa de datos por pantalla

| Pantalla | Función | Información que devuelve |
|---|---|---|
| Búsqueda | `buscar_residentes(termino, estado)` | Residentes coincidentes por nombre, apellido o identificador; incluye estado, cama y piso si están asignados. |
| Reportes | `obtener_reporte_medicamentos()` | Prescripciones con residente, cama, medicamento, dosis indicada, frecuencia, fechas y última administración registrada. |
| Detalle | `obtener_detalle_residente(id_residente)` | Datos personales y de ingreso, cama, habitación, responsable, diagnósticos y prescripciones del residente. |
| Alertas | `obtener_alertas()` | Eventos de bitácora no completados o con prioridad >= 3, con fecha, descripción, habitación y empleado responsable. |
| Vista general | `obtener_resumen()` y `buscar_residentes(estado="Activo")` | Indicadores de residentes/empleados activos, camas disponibles, prescripciones vigentes y listado de residentes activos. |

Las alertas son operativas y se derivan de `BITACORA`; no son diagnósticos ni alertas clínicas.
El reporte muestra prescripciones y la última administración registrada. El modelo actual no define
un horario estructurado de dosis pendientes, por lo que la aplicación no afirma calcular tomas pendientes.
