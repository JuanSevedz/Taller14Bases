import os
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv
from datos import obtener_resumen, buscar_residentes, obtener_reporte_medicamentos, obtener_detalle_residente, obtener_alertas

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "cambiar-esta-clave-localmente")

@app.route("/")
def inicio():
    try:
        resumen = obtener_resumen()
        residentes = buscar_residentes(estado="Activo")
        alertas = obtener_alertas()
        return render_template("index.html", resumen=resumen, residentes=residentes, alertas=alertas[:5])
    except Exception:
        app.logger.exception("Error al cargar la vista general")
        flash("No fue posible consultar la base de datos. Verifique la conexión o contacte al administrador.", "error")
        return render_template("index.html", resumen={}, residentes=[], alertas=[])

@app.route("/residentes")
def residentes():
    q = request.args.get("q", "").strip()
    estado = request.args.get("estado", "").strip()
    try:
        filas = buscar_residentes(termino=q, estado=estado)
    except Exception:
        app.logger.exception("Error en búsqueda")
        flash("No fue posible realizar la búsqueda. Intente nuevamente.", "error")
        filas = []
    return render_template("residentes.html", residentes=filas, q=q, estado=estado)

@app.route("/residentes/<int:id_residente>")
def detalle(id_residente):
    try:
        fila = obtener_detalle_residente(id_residente)
        if not fila:
            flash("No se encontró el residente solicitado.", "warning")
            return render_template("detalle.html", residente=None), 404
        return render_template("detalle.html", residente=fila)
    except Exception:
        app.logger.exception("Error al consultar detalle")
        flash("No fue posible consultar el detalle. Contacte al administrador.", "error")
        return render_template("detalle.html", residente=None), 500

@app.route("/reportes")
def reportes():
    try:
        filas = obtener_reporte_medicamentos()
    except Exception:
        app.logger.exception("Error en reporte")
        flash("No fue posible generar el reporte.", "error")
        filas = []
    return render_template("reportes.html", medicamentos=filas)

@app.route("/alertas")
def alertas():
    try:
        filas = obtener_alertas()
    except Exception:
        app.logger.exception("Error al consultar alertas")
        flash("No fue posible consultar las alertas.", "error")
        filas = []
    return render_template("alertas.html", alertas=filas)

if __name__ == "__main__":
    app.run(host=os.getenv("FLASK_HOST", "127.0.0.1"),
            port=int(os.getenv("FLASK_PORT", "5000")),
            debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
