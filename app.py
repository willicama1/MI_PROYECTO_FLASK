from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hola, Flask está funcionando ✅"

@app.route("/usuario/<nombre>")
def usuario(nombre):
    return f"Bienvenido, {nombre}!"

if __name__ == "__main__":
    app.run(debug=True)
