import os
import pyodbc
from dotenv import load_dotenv
from contextlib import closing

load_dotenv()


class ErrorConsulta(Exception):
    """Error con un mensaje comprensible para el usuario."""


def obtener_conexion():
    cadena = os.environ["BD_ODBC"]
    return pyodbc.connect(cadena, timeout=15)


def conteos():
    sql = """
        SELECT 'TIPO_DOCUMENTO' AS tabla, COUNT(*) AS cantidad FROM public."TIPO_DOCUMENTO"
        UNION ALL
        SELECT 'PARENTESCO', COUNT(*) FROM public."PARENTESCO"
        UNION ALL
        SELECT 'DIRECCION', COUNT(*) FROM public."DIRECCION"
        UNION ALL
        SELECT 'TELEFONO', COUNT(*) FROM public."TELEFONO"
        UNION ALL
        SELECT 'PERSONA', COUNT(*) FROM public."PERSONA"
        UNION ALL
        SELECT 'PERSONA_TELEFONO', COUNT(*) FROM public."PERSONA_TELEFONO"
        UNION ALL
        SELECT 'PERSONA_DIRECCION', COUNT(*) FROM public."PERSONA_DIRECCION"
        UNION ALL
        SELECT 'EMPLEADO', COUNT(*) FROM public."EMPLEADO"
        UNION ALL
        SELECT 'ACUDIENTE', COUNT(*) FROM public."ACUDIENTE"
        UNION ALL
        SELECT 'RESIDENTE', COUNT(*) FROM public."RESIDENTE"
        UNION ALL
        SELECT 'RESIDENTE_ACUDIENTE', COUNT(*) FROM public."RESIDENTE_ACUDIENTE"
        UNION ALL
        SELECT 'ESTADO_CAMA', COUNT(*) FROM public."ESTADO_CAMA"
        UNION ALL
        SELECT 'HABITACION', COUNT(*) FROM public."HABITACION"
        UNION ALL
        SELECT 'CAMA', COUNT(*) FROM public."CAMA"
        UNION ALL
        SELECT 'TURNO', COUNT(*) FROM public."TURNO"
        UNION ALL
        SELECT 'BITACORA', COUNT(*) FROM public."BITACORA"
        UNION ALL
        SELECT 'TIPO_ACTIVIDAD', COUNT(*) FROM public."TIPO_ACTIVIDAD"
        UNION ALL
        SELECT 'ACTIVIDAD', COUNT(*) FROM public."ACTIVIDAD"
        UNION ALL
        SELECT 'PARTICIPACION', COUNT(*) FROM public."PARTICIPACION"
        UNION ALL
        SELECT 'HISTORIAL_MEDICO', COUNT(*) FROM public."HISTORIAL_MEDICO"
        UNION ALL
        SELECT 'ENFERMEDAD', COUNT(*) FROM public."ENFERMEDAD"
        UNION ALL
        SELECT 'DIAGNOSTICO', COUNT(*) FROM public."DIAGNOSTICO"
        UNION ALL
        SELECT 'ALERGIA', COUNT(*) FROM public."ALERGIA"
        UNION ALL
        SELECT 'HISTORIAL_ALERGIA', COUNT(*) FROM public."HISTORIAL_ALERGIA"
        UNION ALL
        SELECT 'MEDICAMENTO', COUNT(*) FROM public."MEDICAMENTO"
        UNION ALL
        SELECT 'PRESCRIPCION', COUNT(*) FROM public."PRESCRIPCION"
        UNION ALL
        SELECT 'ADMINISTRACION_MEDICAMENTO', COUNT(*) FROM public."ADMINISTRACION_MEDICAMENTO"
        ORDER BY tabla;
    """

    try:
        with closing(obtener_conexion()) as conexion:
            with closing(conexion.cursor()) as cursor:
                cursor.execute(sql)
                return cursor.fetchall()

    except pyodbc.Error as error:
        codigo = error.args[0] if error.args else ""
        detalle = str(error).lower()
        

        if "password authentication failed" in detalle:
            mensaje = (
                "No fue posible autenticar la conexión con la base de datos. "
                "Verifique la configuración de acceso."
            )

        elif any(texto in detalle for texto in (
            "could not translate host name",
            "name or service not known",
            "nodename nor servname provided",
            "temporary failure in name resolution",
            "no such host",
            "connection refused",
            "timeout expired",
            "server selection timeout",
        )):
            mensaje = (
                "No se pudo establecer comunicación con el servidor "
                "de la base de datos. Verifique su disponibilidad "
                "o contacte al administrador."
            )

        elif codigo == "42P01":
            mensaje = (
                "No fue posible consultar la información solicitada. "
                "Contacte al administrador."
            )

        else:
            mensaje = (
                "Ocurrió un problema al consultar la base de datos. "
                "Intente nuevamente o contacte al administrador."
            )

        raise ErrorConsulta(mensaje) from None