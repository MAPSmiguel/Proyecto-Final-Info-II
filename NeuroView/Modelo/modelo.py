import sqlite3
import os

class Modelo:

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "..", "neuroview.db")
        self.conexion = sqlite3.connect(db_path)
        self.cursor = self.conexion.cursor()

    def validarUsuario(self, nombre, password, rol):
        self.cursor.execute(
            """
            SELECT *
            FROM usuarios
            WHERE nombre=?
            AND password=?
            AND rol=?
            """,
            (nombre, password, rol)
        )
        return self.cursor.fetchone()
