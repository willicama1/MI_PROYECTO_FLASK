from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
import csv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --------------------------
# CONFIGURACIÓN BASE DE DATOS
# --------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para SQLite
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100))

with app.app_context():
    db.create_all()

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

    # 4. Guardar en SQLite
    nuevo_usuario = Usuario(nombre=nombre, correo=correo)
    db.session.add(nuevo_usuario)
    db.session.commit()

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
    usuarios = Usuario.query.all()
    if usuarios:
        return "<br>".join([f"{u.nombre} - {u.correo}" for u in usuarios])
    return "No hay datos en la base de datos."

if __name__ == "__main__":
    app.run(debug=True)
