import os
import pyodbc

def obtener_conexion():
    cadena = os.getenv("BD_ODBC")
    if not cadena:
        raise RuntimeError("No está definida la variable BD_ODBC.")
    return pyodbc.connect(cadena, timeout=15)

def _consultar(sql, parametros=(), uno=False):
    cn = obtener_conexion()
    try:
        cur = cn.cursor()
        try:
            cur.execute(sql, parametros)
            columnas = [c[0] for c in cur.description] if cur.description else []
            filas = cur.fetchone() if uno else cur.fetchall()
            if uno:
                return dict(zip(columnas, filas)) if filas else None
            return [dict(zip(columnas, fila)) for fila in filas]
        finally:
            cur.close()
    finally:
        cn.close()

def obtener_resumen():
    sql = '''
    SELECT
      (SELECT COUNT(*) FROM "RESIDENTE" WHERE "estado"='Activo') AS residentes_activos,
      (SELECT COUNT(*) FROM "EMPLEADO" WHERE "estado"='Activo') AS empleados_activos,
      (SELECT COUNT(*) FROM "CAMA" c JOIN "ESTADO_CAMA" ec
       ON ec."ID_estado_cama"=c."FK_estado_cama"
       WHERE ec."nombre_estado"='Disponible') AS camas_disponibles,
      (SELECT COUNT(*) FROM "PRESCRIPCION"
       WHERE "fecha_prescripcion"<=CURRENT_DATE
       AND ("fecha_fin" IS NULL OR "fecha_fin">=CURRENT_DATE)) AS prescripciones_vigentes
    '''
    return _consultar(sql, uno=True) or {}

def buscar_residentes(termino="", estado=""):
    sql = '''
    SELECT r."ID_residente" AS id_residente, p."nombre_persona" AS nombre_persona,
      p."apellido_persona" AS apellido_persona, r."estado" AS estado,
      r."fecha_ingreso" AS fecha_ingreso, c."codigo_cama" AS codigo_cama,
      h."piso_habitacion" AS piso
    FROM "RESIDENTE" r
    JOIN "PERSONA" p ON p."ID_persona"=r."FK_persona"
    LEFT JOIN "CAMA" c ON c."ID_cama"=r."FK_cama"
    LEFT JOIN "HABITACION" h ON h."ID_habitacion"=c."FK_habitacion"
    WHERE (?='' OR CAST(r."ID_residente" AS TEXT) ILIKE ?
      OR p."nombre_persona" ILIKE ? OR p."apellido_persona" ILIKE ?
      OR (p."nombre_persona" || ' ' || p."apellido_persona") ILIKE ?)
      AND (?='' OR r."estado"=?)
    ORDER BY p."apellido_persona", p."nombre_persona"
    '''
    patron = f"%{termino}%"
    return _consultar(sql, (termino, patron, patron, patron, patron, estado, estado))

def obtener_detalle_residente(id_residente):
    sql = '''
    SELECT r."ID_residente" AS id_residente, r."estado" AS estado,
      r."fecha_ingreso" AS fecha_ingreso, p."nombre_persona" AS nombre_persona,
      p."apellido_persona" AS apellido_persona, p."numero_documento" AS numero_documento,
      p."correo" AS correo, c."codigo_cama" AS codigo_cama,
      h."piso_habitacion" AS piso, ec."nombre_estado" AS estado_cama,
      ep."nombre_persona" AS responsable, em."rol_empleado" AS rol_responsable
    FROM "RESIDENTE" r
    JOIN "PERSONA" p ON p."ID_persona"=r."FK_persona"
    LEFT JOIN "CAMA" c ON c."ID_cama"=r."FK_cama"
    LEFT JOIN "HABITACION" h ON h."ID_habitacion"=c."FK_habitacion"
    LEFT JOIN "ESTADO_CAMA" ec ON ec."ID_estado_cama"=c."FK_estado_cama"
    LEFT JOIN "EMPLEADO" em ON em."ID_empleado"=r."FK_empleado_responsable"
    LEFT JOIN "PERSONA" ep ON ep."ID_persona"=em."FK_persona"
    WHERE r."ID_residente"=?
    '''
    residente = _consultar(sql, (id_residente,), uno=True)
    if not residente:
        return None
    residente["medicamentos"] = _consultar('''
      SELECT m."nombre" AS medicamento, pr."dosis_indicada" AS dosis,
        pr."frecuencia" AS frecuencia, pr."fecha_prescripcion" AS fecha_prescripcion,
        pr."fecha_fin" AS fecha_fin, pr."indicaciones" AS indicaciones
      FROM "HISTORIAL_MEDICO" hm
      JOIN "PRESCRIPCION" pr ON pr."FK_historial"=hm."ID_historial"
      JOIN "MEDICAMENTO" m ON m."ID_medicamento"=pr."FK_medicamento"
      WHERE hm."FK_residente"=? ORDER BY pr."fecha_prescripcion" DESC
    ''', (id_residente,))
    residente["diagnosticos"] = _consultar('''
      SELECT en."nombre_enfermedad" AS enfermedad,
        d."fecha_diagnostico" AS fecha_diagnostico, d."observaciones" AS observaciones
      FROM "HISTORIAL_MEDICO" hm
      JOIN "DIAGNOSTICO" d ON d."FK_historial"=hm."ID_historial"
      JOIN "ENFERMEDAD" en ON en."ID_enfermedad"=d."FK_enfermedad"
      WHERE hm."FK_residente"=? ORDER BY d."fecha_diagnostico" DESC
    ''', (id_residente,))
    return residente

def obtener_reporte_medicamentos():
    sql = '''
    SELECT p."nombre_persona" || ' ' || p."apellido_persona" AS residente,
      c."codigo_cama" AS codigo_cama, m."nombre" AS medicamento,
      pr."dosis_indicada" AS dosis_indicada, pr."frecuencia" AS frecuencia,
      pr."fecha_prescripcion" AS fecha_prescripcion, pr."fecha_fin" AS fecha_fin,
      (SELECT MAX(am."fecha_aplicacion") FROM "ADMINISTRACION_MEDICAMENTO" am
       WHERE am."FK_prescripcion"=pr."ID_prescripcion") AS ultima_administracion
    FROM "PRESCRIPCION" pr
    JOIN "HISTORIAL_MEDICO" hm ON hm."ID_historial"=pr."FK_historial"
    JOIN "RESIDENTE" r ON r."ID_residente"=hm."FK_residente"
    JOIN "PERSONA" p ON p."ID_persona"=r."FK_persona"
    LEFT JOIN "CAMA" c ON c."ID_cama"=r."FK_cama"
    JOIN "MEDICAMENTO" m ON m."ID_medicamento"=pr."FK_medicamento"
    ORDER BY p."apellido_persona", m."nombre"
    '''
    return _consultar(sql)

def obtener_alertas():
    sql = '''
    SELECT b."ID_bitacora" AS id_alerta, b."fecha_hora" AS fecha_hora,
      b."tipo_evento" AS tipo_evento, b."descripcion" AS descripcion,
      b."estado" AS estado, b."nivel_prioridad" AS prioridad,
      h."piso_habitacion" AS piso,
      ep."nombre_persona" || ' ' || ep."apellido_persona" AS empleado
    FROM "BITACORA" b
    JOIN "HABITACION" h ON h."ID_habitacion"=b."FK_habitacion"
    JOIN "EMPLEADO" e ON e."ID_empleado"=b."FK_empleado"
    JOIN "PERSONA" ep ON ep."ID_persona"=e."FK_persona"
    WHERE COALESCE(b."estado",'')<>'Completado'
       OR COALESCE(b."nivel_prioridad",0)>=3
    ORDER BY b."nivel_prioridad" DESC NULLS LAST, b."fecha_hora" DESC
    '''
    return _consultar(sql)
