import mysql.connector

def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="22deNoviembre@",
        database="desarrollo_web"
    )
    return conexion
