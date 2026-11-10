import os
import pyodbc
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

ODBC_CONNECTION_STRING = os.getenv("ODBC_CONNECTION_STRING")

def get_db_connection():
    return pyodbc.connect(ODBC_CONNECTION_STRING)

@app.route('/api/residentes', methods=['GET'])
def get_residentes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT R."ID_residente" AS id_residente, 
                   P."nombre_persona" AS nombre_persona, 
                   P."apellido_persona" AS apellido_persona, 
                   C."codigo_cama" AS codigo_cama, 
                   R."estado" AS estado 
            FROM "RESIDENTE" R
            JOIN "PERSONA" P ON R."FK_persona" = P."ID_persona"
            LEFT JOIN "CAMA" C ON R."FK_cama" = C."ID_cama";
        """)
        columns = [column[0].lower() for column in cursor.description]
        residentes = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        return jsonify(residentes)
    except Exception as e:
        print("Error en residentes (pyodbc):", e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/medicamentos-pendientes', methods=['GET'])
def get_medicamentos_pendientes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Pr."frecuencia" AS hora_programada, 
                   (Pers."nombre_persona" || ' ' || Pers."apellido_persona") AS residente, 
                   C."codigo_cama" AS codigo_cama, 
                   M."nombre" AS medicamento, 
                   Pr."dosis_indicada" AS dosis
            FROM "ADMINISTRACION_MEDICAMENTO" AM
            JOIN "PRESCRIPCION" Pr ON AM."FK_prescripcion" = Pr."ID_prescripcion"
            JOIN "HISTORIAL_MEDICO" H ON Pr."FK_historial" = H."ID_historial"
            JOIN "RESIDENTE" R ON H."FK_residente" = R."ID_residente"
            JOIN "PERSONA" Pers ON R."FK_persona" = Pers."ID_persona"
            LEFT JOIN "CAMA" C ON R."FK_cama" = C."ID_cama"
            JOIN "MEDICAMENTO" M ON Pr."FK_medicamento" = M."ID_medicamento";
        """)
        columns = [column[0].lower() for column in cursor.description]
        medicamentos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        return jsonify(medicamentos)
    except Exception as e:
        print("Error en medicamentos (pyodbc):", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)