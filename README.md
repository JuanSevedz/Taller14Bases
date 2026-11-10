# Proyecto de Bases de Datos — Sistema de Gestión Geriátrico

Repositorio académico del proyecto de Bases de Datos. Contiene el script SQL del modelo, las pruebas de conexión y consulta, y una aplicación web desarrollada con Flask para consultar la información almacenada en PostgreSQL (Neon).

## 1. Contenido del repositorio

```text
.
├── conexion.py              # Prueba/funciones de conexión del trabajo inicial
├── datos.py                 # Capa de datos del programa inicial
├── Gerioatrico.sql          # Script SQL de la base de datos
├── main.py                  # Programa de prueba inicial
├── punto4/                  # Aplicación web Flask del Punto 4
│   ├── app.py               # Servidor web y rutas
│   ├── datos.py             # Consultas SQL de la aplicación Flask
│   ├── requirements.txt     # Dependencias Python
│   ├── .env.ejemplo         # Plantilla de configuración, sin credenciales reales
│   ├── README.md            # Instrucciones específicas de la aplicación
│   ├── PUNTO_4_ARQUITECTURA.md
│   ├── static/              # CSS
│   └── templates/           # Plantillas HTML
└── TEST1/                   # Archivos de pruebas anteriores

```

Los directorios `__pycache__/`, los archivos `.pyc`, el entorno virtual `.venv/` y el archivo `.env` local no deben compartirse en Git.

## 2. Requisitos para probar la aplicación

El compañero que clone el repositorio necesita:

* Python 3.10 o superior.
* Git.
* Acceso a Internet.
* Controlador ODBC de PostgreSQL **psqlODBC**, registrado con el nombre `PostgreSQL Unicode`.
* Credenciales de acceso a la base PostgreSQL en Neon del proyecto.

> La aplicación Flask se ejecuta desde `punto4/`. No es necesario ejecutar `main.py` para probar las pantallas web.

## 3. Clonar el repositorio

Desde una terminal, clona el repositorio y entra a la carpeta raíz:

```bash
git clone https://github.com/JuanSevedz/Taller14Bases
cd Taller14Bases

```

Los siguientes pasos se ejecutan desde esta carpeta raíz, salvo cuando se indique expresamente entrar a `punto4/`. El controlador psqlODBC se instala en el sistema operativo; las dependencias Python de Flask se instalan desde `punto4/`, porque allí está `requirements.txt`.

## 4. Instalar el controlador psqlODBC

Este paso se puede realizar desde cualquier directorio: instala un controlador del sistema operativo, no un paquete del proyecto.

La aplicación utiliza `pyodbc`, que necesita que el controlador ODBC de PostgreSQL esté instalado en el sistema operativo. Instalar el paquete Python `pyodbc` por sí solo no instala psqlODBC.

### Ubuntu

Instala el administrador ODBC y el controlador:

```bash
sudo apt update
sudo apt install unixodbc unixodbc-dev odbc-postgresql

```

Comprueba que el controlador esté registrado:

```bash
odbcinst -q -d

```

Debe aparecer un controlador llamado:

```text
[PostgreSQL Unicode]

```

Si el nombre registrado es distinto, hay que ajustar el valor `Driver={...}` en la cadena `BD_ODBC` del archivo `.env`.

### Windows

Instala la versión de psqlODBC que corresponda a la arquitectura de Python (32 o 64 bits) y comprueba en el administrador de orígenes de datos ODBC que aparezca el controlador PostgreSQL Unicode. Después configura la cadena `BD_ODBC` con el nombre exacto registrado.

## 5. Preparar el entorno Python

Entra a la carpeta de la aplicación:

```bash
cd punto4

```

Crea y activa un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate

```

En Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1

```

Instala las dependencias:

```bash
pip install -r requirements.txt

```

## 6. Configurar la conexión con Neon

Dentro de `punto4/`, copia el archivo de ejemplo:

```bash
cp .env.ejemplo .env

```

En Windows PowerShell:

```powershell
Copy-Item .env.ejemplo .env

```

Abre `.env` con un editor y completa los datos de conexión entregados de forma segura por el responsable del proyecto:

```env
BD_ODBC=Driver={PostgreSQL Unicode};Server=HOST_DE_NEON;Port=5432;Database=NOMBRE_BASE;Uid=USUARIO;Pwd=CONTRASENA;sslmode=require;UseServerSidePrepare=0;
FLASK_SECRET_KEY=una-clave-local-larga-y-aleatoria
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=false

```

Consideraciones:

* Sustituye los valores de ejemplo por las credenciales reales de Neon.
* Conserva `sslmode=require`.
* Conserva `UseServerSidePrepare=0`; se agregó para evitar el conflicto de sentencias preparadas que se presentó durante las pruebas con Neon y psqlODBC.
* No publiques, envíes por Git ni adjuntes el archivo `.env`.
* No escribas la contraseña en el código fuente, capturas de pantalla ni documentos de entrega.
* Si el responsable de la base de datos no ha compartido las credenciales, solicítalas por un canal privado. No las publiques en el repositorio.

## 7. Ejecutar la aplicación

Asegúrate de seguir dentro de `punto4/` y de tener activo el entorno virtual creado allí:

```bash
python app.py

```

En el navegador abre:

```text
http://127.0.0.1:5000

```

Para detener el servidor, regresa a la terminal y presiona `Ctrl + C`.

Si abres una terminal nueva y vuelves a probar la aplicación, recuerda activar el entorno virtual y entrar a `punto4/` antes de ejecutar `python app.py`.

## 8. Pruebas funcionales que debe realizar el compañero

La aplicación es de consulta. Para probarla, utiliza las opciones del menú superior:

| Prueba | Qué hacer | Resultado esperado |
| --- | --- | --- |
| Vista general | Entrar a `[http://127.0.0.1:5000/](http://127.0.0.1:5000/)` | Se muestran los indicadores y el listado de residentes activos, si existen registros que cumplan el filtro. |
| Búsqueda | Entrar a **Residentes**, buscar por nombre, apellido o ID; probar también el filtro de estado | La tabla muestra coincidencias o un mensaje indicando que no hay resultados. |
| Detalle | Desde la tabla de residentes, seleccionar **Consultar** o abrir `/residentes/ID` usando un ID existente | Se presenta la información del residente, su ubicación, diagnósticos y prescripciones disponibles. |
| Reportes | Entrar a **Reportes** | Se muestra el listado de prescripciones y la última administración registrada, si existe. |
| Alertas | Entrar a **Alertas** | Se muestran eventos de bitácora no completados o con prioridad igual o superior a 3, según la consulta implementada. |

Para probar el detalle, utiliza un identificador que exista en la tabla `RESIDENTE`. No se debe asumir que el ID `1` está registrado en todas las bases de datos.

### Alcance funcional

* La aplicación consulta la base de datos; no inserta, modifica ni elimina registros.
* Las alertas son operativas y se derivan de la bitácora. No representan diagnósticos ni alertas clínicas.
* El reporte presenta prescripciones y la última administración registrada. No calcula dosis pendientes ni horarios de toma.
* La cantidad de filas y los resultados dependen de los datos que estén actualmente almacenados en Neon.

## 9. Solución de problemas

### `pyodbc.InterfaceError` o no se encuentra el controlador

Comprueba que psqlODBC esté instalado y que el nombre coincida exactamente con el de `Driver={...}` en `.env`:

```bash
odbcinst -q -d

```

### Error de autenticación

Verifica el host, nombre de la base de datos, usuario y contraseña en `.env`. Comprueba que no haya espacios adicionales ni caracteres omitidos. No compartas la contraseña para solicitar ayuda.

### Error de conexión SSL o servidor

Verifica el acceso a Internet, el hostname de Neon, el puerto `5432` y que la cadena incluya `sslmode=require`.

### Error de sentencias preparadas de PostgreSQL

Confirma que la cadena ODBC contenga:

```text
UseServerSidePrepare=0;

```

Después detén y vuelve a iniciar Flask.

### La página muestra un error de consulta o no hay datos

Revisa la terminal donde se ejecuta `python app.py`: allí se registra el error técnico. Comprueba que se esté usando la base de datos del proyecto y que el esquema y sus tablas estén creados. Un resultado vacío no necesariamente significa que Flask esté fallando; puede que no existan registros que cumplan el filtro.

## 10. Seguridad y archivos ignorados por Git

El `.gitignore` ubicado en la raíz del repositorio debe ignorar archivos locales como:

```gitignore
.env
.venv/
venv/
__pycache__/
*.py[cod]
.pytest_cache/

```

Como los patrones anteriores no están anclados a la raíz, Git también ignora esos nombres dentro de `punto4/`. Por tanto, el archivo `punto4/.env` y el entorno `punto4/.venv/` no deben aparecer en los commits. El archivo `punto4/.env.ejemplo` sí debe permanecer versionado: su nombre no coincide con el patrón exacto `.env`.

Esto significa que cada integrante debe crear su propio entorno virtual y su propio `.env` después de clonar el repositorio.

**Importante:** `.gitignore` no elimina archivos que ya hayan sido confirmados (commit) y enviados al repositorio. Si un `.env` con credenciales reales fue publicado alguna vez, hay que cambiar/rotar esas credenciales y retirar el archivo del seguimiento de Git. No basta con agregarlo después a `.gitignore`.

El archivo `.env.ejemplo` sí se versiona porque contiene únicamente valores de muestra.

## 11. Arquitectura resumida

```text
Navegador (HTML/CSS)
        |
        | HTTP
        v
Servidor web: Flask (Python)
        |
        v
Capa de datos: punto4/datos.py
        |
        v
pyodbc
        |
        v
Controlador psqlODBC
        |
        v
PostgreSQL en Neon

```

El navegador no se conecta directamente a PostgreSQL ni recibe las credenciales. Las consultas SQL y la conexión están centralizadas en la capa de datos.