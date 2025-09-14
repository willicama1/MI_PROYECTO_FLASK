from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
import csv
from Conexion.conexion import obtener_conexion

app = Flask(__name__)

# --------------------------
# RUTAS PRINCIPALES
# --------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/usuario/<nombre>")
def usuario(nombre):
    return f"Bienvenido, {nombre}!"

@app.route("/formulario")
def formulario():
    return render_template("formulario.html")

@app.route("/resultado")
def resultado():
    return render_template("resultado.html")

# --------------------------
# PRUEBA DE CONEXIÓN A MYSQL
# --------------------------
@app.route("/test_db")
def test_db():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT DATABASE();")
        resultado = cursor.fetchone()
        conexion.close()
        return f"Conexión exitosa a la base de datos: {resultado[0]}"
    except Exception as e:
        return f"Error en la conexión: {str(e)}"

# --------------------------
# GUARDAR DATOS EN DIFERENTES FORMATOS
# --------------------------
@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form['nombre']
    correo = request.form['correo']

    # 1. Guardar en TXT
    with open("datos/datos.txt", "a") as f:
        f.write(f"{nombre} - {correo}\n")

    # 2. Guardar en JSON
    json_file = "datos/datos.json"
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            datos_json = json.load(f)
    else:
        datos_json = []
    datos_json.append({"nombre": nombre, "correo": correo})
    with open(json_file, "w") as f:
        json.dump(datos_json, f, indent=4)

    # 3. Guardar en CSV
    with open("datos/datos.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nombre, correo])

    # 4. Guardar en MySQL
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo) VALUES (%s, %s)",
            (nombre, correo)
        )
        conexion.commit()
        conexion.close()
    except Exception as e:
        return f"Error guardando en MySQL: {str(e)}"

    return redirect(url_for("resultado"))

# --------------------------
# LEER DATOS
# --------------------------
@app.route("/ver_txt")
def ver_txt():
    if os.path.exists("datos/datos.txt"):
        with open("datos/datos.txt", "r") as f:
            contenido = f.readlines()
        return "<br>".join(contenido)
    return "No hay datos en TXT."

@app.route("/ver_json")
def ver_json():
    if os.path.exists("datos/datos.json"):
        with open("datos/datos.json", "r") as f:
            datos = json.load(f)
        return jsonify(datos)
    return jsonify([])

@app.route("/ver_csv")
def ver_csv():
    if os.path.exists("datos/datos.csv"):
        with open("datos/datos.csv", "r") as f:
            lector = csv.reader(f)
            filas = list(lector)
        return str(filas)
    return "No hay datos en CSV."

@app.route("/ver_db")
def ver_db():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, correo FROM usuarios")
        usuarios = cursor.fetchall()
        conexion.close()
        if usuarios:
            return "<br>".join([f"{u[0]} - {u[1]}" for u in usuarios])
        return "No hay datos en la base de datos."
    except Exception as e:
        return f"Error leyendo MySQL: {str(e)}"

# --------------------------
# EJECUTAR APP
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)
