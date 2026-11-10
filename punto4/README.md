# Sistema de Gestión Geriátrico — Flask + PostgreSQL

Aplicación web de consulta para el proyecto académico.

## Tecnologías
- Python 3.10+
- Flask
- pyodbc
- Controlador psqlODBC (PostgreSQL Unicode)
- PostgreSQL en Neon

## Preparación en Ubuntu
Instale psqlODBC y verifique el nombre del controlador:
```bash
odbcinst -q -d
```
Si el nombre no es `PostgreSQL Unicode`, ajuste `Driver={...}` en `.env`.

Cree y active el entorno:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure las credenciales:
```bash
cp .env.ejemplo .env
nano .env
```
Complete servidor, base, usuario y contraseña de Neon. Mantenga `sslmode=require`.
**No entregue ni suba el archivo `.env` real.** El archivo `.env.ejemplo` sí se entrega porque
solo contiene marcadores.

Ejecute:
```bash
python app.py
```
Abra `http://127.0.0.1:5000` y detenga con `Ctrl+C`.

## Pantallas
- Vista general: indicadores, residentes activos y alertas recientes.
- Búsqueda: filtra por nombre, apellido, identificador y estado.
- Detalle: datos personales, cama/habitación, responsable, diagnósticos y prescripciones.
- Reportes: prescripciones y última administración registrada.
- Alertas: eventos de bitácora no completados o con prioridad igual o superior a 3.

Las alertas son operativas, no clínicas. El reporte no calcula dosis pendientes ni horarios de toma:
el esquema no contiene un calendario estructurado de administración. Esta versión es de consulta;
no realiza INSERT, UPDATE ni DELETE.

Todas las consultas SQL están centralizadas en `datos.py`. El navegador nunca recibe la cadena
de conexión: Flask carga `BD_ODBC` desde `.env` en el servidor.
