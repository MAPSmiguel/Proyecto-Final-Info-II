import sys

from PyQt5.QtWidgets import QApplication

from Vista.vista import VistaBienvenida
from Modelo.modelo import Modelo
from Controlador.controlador import Controlador

app = QApplication(sys.argv)

vista = VistaBienvenida()

modelo = Modelo()

controlador = Controlador(
    vista,
    modelo
)

vista.show()

sys.exit(app.exec_())