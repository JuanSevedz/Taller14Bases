import os
import pyodbc
from dotenv import load_dotenv
from contextlib import closing

# Cargar las variables del archivo .env
load_dotenv()


def comprobar_conexion():
    cadena = os.environ["BD_ODBC"]

    try:
        with closing(pyodbc.connect(cadena, timeout=15)) as conexion:
            with closing(conexion.cursor()) as cursor:

                sql = """
                    SELECT
                        current_database(),
                        current_user,
                        version();
                """

                cursor.execute(sql)

                base, usuario, version = cursor.fetchone()

                print("CONEXIÓN EXITOSA")
                print("------------------------------")
                print(f"Base de datos: {base}")
                print(f"Usuario: {usuario}")
                print(f"Versión de PostgreSQL: {version}")

    except pyodbc.Error as error:
        print("No fue posible conectarse a la base de datos.")
        print(f"Código del error: {error.args[0]}")
        print(f"Detalle técnico: {error}")


if __name__ == "__main__":
    comprobar_conexion()
