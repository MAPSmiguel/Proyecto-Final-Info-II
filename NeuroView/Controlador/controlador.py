
# El controlador es el intermediario entre la Vista y el Modelo.
# La vista le dice "el usuario hizo clic en X"
# y el controlador decide que hacer: llama al modelo,
# procesa la respuesta y le dice a la vista que mostrar.

from PyQt5.QtWidgets import QMessageBox
from Vista.vista import (
    VistaDashboard,
    VistaDicom,
    VistaSenales,
    VistaDatos
)


class Controlador:

    def __init__(self, vista, modelo):

        self.__vista  = vista   # esta es la VistaBienvenida (login)
        self.__modelo = modelo

        # Le damos al controlador a la vista para que ella pueda llamarlo
        self.__vista.setControlador(self)

        # Declaramos las ventanas secundarias como None por ahora
        # Se crean cuando el usuario las pida, no antes
        # Si las creo aqui, se abririan todas al inicio sin que nadie las pidiera
        self.__dashboard     = None
        self.__vistaDicom    = None
        self.__vistaSenales  = None
        self.__vistaDatos    = None


    def validarLogin(self, usuario, password, rol):

        # Le preguntamos al modelo si ese usuario existe en la base de datos
        resultado = self.__modelo.validarUsuario(usuario, password, rol)

        if resultado:
            #Escondemos la ventana de bienvenida (no la cerramos,
            #    porque si la cerramos la app podria terminar)
            self.__vista.hide()

            #  Creamos el dashboard y le asignamos el controlador
            self.__dashboard = VistaDashboard()
            self.__dashboard.setControlador(self)

            #  Mostramos el dashboard
            self.__dashboard.show()

        else:
            QMessageBox.warning(
                self.__vista,
                "Error de acceso",
                "Usuario o contraseña incorrectos.\nVerifica tus datos e intenta de nuevo."
            )

    # Cada metodo crea la ventana correspondiente,
    # le asigna el controlador y la muestra.
    #
    #  guardamos en self.__vistaDicom porque si hacemos
    #     ventana = VistaDicom()
    #     ventana.show()
    # Python destruye ventana al terminar el metodo
    # Al guardarla en self.__vistaDicom, el controlador
    # la sostiene en memoria 

    def abrirModuloDicom(self):
        # Creamos la ventana DICOM
        self.__vistaDicom = VistaDicom()
        # Le damos el controlador para que pueda llamarnos cuando el usuario haga algo
        self.__vistaDicom.setControlador(self)
        self.__vistaDicom.show() #mostramos

    def abrirModuloSenales(self):
        self.__vistaSenales = VistaSenales()
        self.__vistaSenales.setControlador(self)
        self.__vistaSenales.show()

    def abrirModuloDatos(self):
        self.__vistaDatos = VistaDatos()
        self.__vistaDatos.setControlador(self)
        self.__vistaDatos.show()


    # esto lo coloca migeu y michel conectandolo al modelo


    def cargarDicom(self):
        #  abrir dialogo de archivo, llamar al modelo para cargar, actualizar los sliders con el numero de cortes, mostrar la imagen
        pass

    def convertirNifti(self):
        #  llamar al modelo para que convierta el DICOM cargado a NIfTI
        pass

    def mostrarCorteAxial(self, valor):
        #  pedirle al modelo el corte numero "valor" en el eje axial y mostrar la imagen resultante en la VistaDicom
        pass

    def mostrarCorteCoronal(self, valor):
        pass

    def mostrarCorteSagital(self, valor):
        pass

    def guardarZoom(self, nombre):
        # decirle al modelo que recorte y guarde la imagen con ese nombre
        pass

    def segmentar(self, metodo):
        #  decirle al modelo que aplique el threshold elegido
        pass

    def aplicarMorfologia(self, operacion, kernel):
        # decirle al modelo que aplique la transformacion morfologica
        pass

        #metodos de señales


    def cargarMat(self):
        #  abrir dialogo de archivo .mat y llamar al modelo
        pass

    def procesarSenales(self, inicio, fin, eje):
        #  llamar al modelo con los canales y el eje elegidos
        # y mostrar los graficos en la VistaSenales
        pass


    # datos tabulares
  

    def cargarCSV(self):
        # abrir dialogo de archivo .csv y llamar al modelo
        pass

    def cargarExcel(self):
        #  abrir dialogo de archivo .xlsx y llamar al modelo
        pass

    def graficarScatter(self, x, y):
        #  decirle al modelo que grafique scatter entre columna x y columna y
        pass
