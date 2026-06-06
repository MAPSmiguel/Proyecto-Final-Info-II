
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog
)

from PyQt5.uic import loadUi

class VistaBienvenida(QMainWindow):

    def __init__(self):
        super().__init__()
        # Cargamos el diseño de Qt Designer
        loadUi("Vista/Bienvenida.ui", self)

        #  Si se pulsa ingresar llamamos al metodo ingresar
        self.btnIngresar.clicked.connect(
            self.ingresar
        )

    def ingresar(self):
        # Leemos lo que escribio el usuario en los campos del .ui
        usuario  = self.input_usuario.text()
        password = self.input_password.text()
        rol      = self.combo_rol.currentText()

        # Le pasamos los datos al controlador para que el valide
        # La vista no sabe si el usuario existe o no eso lo decide el controlador en su codigo
        self.__controlador.validarLogin(usuario, password, rol)

    def setControlador(self, c):
        #se crea el atributo porque puede que eocntrolador aun no exista 
        # asi la vista y el controlador se conocen entre si
        self.__controlador = c


class VistaDashboard(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi("Vista/dashboard.ui", self)

        # Cada boton llama a su metodo 
        self.btnDicom.clicked.connect(
            self.abrirDicom
        )

        self.btnsenales.clicked.connect(
            self.abrirSenales
        )

        self.btnDatos.clicked.connect(
            self.abrirDatos
        )

        # El boton cierra esta ventana
        self.btnSalir.clicked.connect(
            self.close
        )

    def abrirDicom(self):
        # Le decimos al controlador que el usuario quiere abrir el modulo DICOM
        # El controlador crea y muestra esa ventana
        self.__controlador.abrirModuloDicom()

    def abrirSenales(self):
        # Lo mismo para señales
        self.__controlador.abrirModuloSenales()

    def abrirDatos(self):
        # Lo mismo pero para datos tabulares
        self.__controlador.abrirModuloDatos()

    def setControlador(self, c):
        self.__controlador = c

# A carga archivos .dcm, ve los 3 cortes
# (axial, coronal, sagital) con sliders, y puede convertir a NIfTI.

class VistaDicom(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi("Vista/dicom.ui", self)

        self.btnCargarDicom.clicked.connect(
            self.cargarDicom
        )

        self.btnConvertirNifti.clicked.connect(
            self.convertirNifti
        )

        # Los sliders estan conectados a metodos que avisan que corte mostrar
        self.sliderAxial.valueChanged.connect(
            self.corteAxial
        )

        self.sliderCoronal.valueChanged.connect(
            self.corteCoronal
        )

        self.sliderSagital.valueChanged.connect(
            self.corteSagital
        )

    def cargarDicom(self):
        # Le dice al controlador que el usuario quiere cargar un DICOM
        self.__controlador.cargarDicom()

    def convertirNifti(self):
        self.__controlador.convertirNifti()

    def corteAxial(self, valor):
        # Cada vez que el usuario mueve el slider, le mandamos el valor al controlador
        # El controlador le dira al modelo que procese ese corte y luego
        # le devolvera la imagen a esta vista para mostrarla
        self.__controlador.mostrarCorteAxial(valor)

    def corteCoronal(self, valor):
        self.__controlador.mostrarCorteCoronal(valor)

    def corteSagital(self, valor):
        self.__controlador.mostrarCorteSagital(valor)

    def setControlador(self, c):
        self.__controlador = c


#donde el usuario recorta una region de la imagen DICOM y la guarda con un nombre.

class VistaZoom(QDialog):

    def __init__(self):
        super().__init__()
        loadUi("Vista/zoom.ui", self)

        self.btnGuardarZoom.clicked.connect(
            self.guardarZoom
        )

    def guardarZoom(self):
        # Leemos el nombre que escribio el usuario para guardar la imagen
        nombre = self.txtNombreImagen.text()
        self.__controlador.guardarZoom(nombre)

    def setControlador(self, c):
        self.__controlador = c


# El usuario elige el tipo de binarizacion desde un QComboBox
# y le aplica un umbral a la imagen DICOM recortada.

class VistaSegmentacion(QDialog):

    def __init__(self):
        super().__init__()
        loadUi("Vista/Segmentacion.ui", self)

        self.btnSegmentar.clicked.connect(
            self.segmentar
        )

    def segmentar(self):
        # Leemos cual opcion eligio el usuario
        #Binario, Binario Invertido,...
        metodo = self.cmbThreshold.currentText()
        self.__controlador.segmentar(metodo)

    def setControlador(self, c):
        self.__controlador = c


# El usuario elige la operacion morfologica (apertura, cierre,
# gradiente, erosion...) y el tamaño del kernel con un QSpinBox.


class VistaMorfologia(QDialog):

    def __init__(self):
        super().__init__()
        loadUi("Vista/morfologia.ui", self)

        self.btnAplicar.clicked.connect(
            self.aplicar
        )

    def aplicar(self):
        # Leemos la operacion del combo y el tamaño del kernel del spinbox
        operacion = self.cmbMorfologia.currentText()
        kernel    = self.spinKernel.value()
        self.__controlador.aplicarMorfologia(operacion, kernel)

    def setControlador(self, c):
        self.__controlador = c



# El usuario carga un archivo .mat con señales biomedicas (ECG/EEG),
# selecciona canales, agrega ruido y ve estadisticas.

class VistaSenales(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi("Vista/senales.ui", self)

        self.btnCargarMat.clicked.connect(
            self.cargarMat
        )

        self.btnProcesar.clicked.connect(
            self.procesar
        )

    def cargarMat(self):
        self.__controlador.cargarMat()

    def procesar(self):
        # Leemos los valores de los controles de la interfaz
        inicio = self.spinCanalInicial.value()
        fin    = self.spinCanalFinal.value()

        # Los RadioButtons dicen sobre que eje queremos calcular
        # el promedio y desviacion estandar (requerimiento 8c )
        if self.radioEje0.isChecked():
            eje = 0
        elif self.radioEje1.isChecked():
            eje = 1
        else:
            eje = 2

        self.__controlador.procesarSenales(inicio, fin, eje)

    def setControlador(self, c):
        self.__controlador = c


# El usuario carga un CSV o Excel con datos medicos,
# ve la info/describe del archivo, hace plots y scatter.

class VistaDatos(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi("Vista/datos.ui", self)

        self.btnCargarCSV.clicked.connect(
            self.cargarCSV
        )

        self.btnCargarExcel.clicked.connect(
            self.cargarExcel
        )

        self.btnScatter.clicked.connect(
            self.scatter
        )

    def cargarCSV(self):
        self.__controlador.cargarCSV()

    def cargarExcel(self):
        self.__controlador.cargarExcel()

    def scatter(self):
        # Leemos las dos columnas elegidas por el usuario en los combos
        x = self.cmbX.currentText()
        y = self.cmbY.currentText()
        self.__controlador.graficarScatter(x, y)

    def setControlador(self, c):
        self.__controlador = c
    def graficadoraCanvas(self,canvas):
        pass
