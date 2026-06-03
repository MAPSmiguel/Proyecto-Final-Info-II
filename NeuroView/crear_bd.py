import sqlite3

conexion = sqlite3.connect("neuroview.db")

cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    password TEXT NOT NULL,
    rol TEXT NOT NULL
)
""")

cursor.execute("""
INSERT INTO usuarios(nombre,password,rol)
VALUES('admin','1234','Administrador')
""")

cursor.execute("""
INSERT INTO usuarios(nombre,password,rol)
VALUES('usuario','1234','Usuario')
""")

conexion.commit()
conexion.close()

print("Base de datos NeuroView creada")