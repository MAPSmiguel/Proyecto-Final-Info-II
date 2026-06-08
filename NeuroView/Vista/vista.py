import os
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog, QVBoxLayout, QTableWidgetItem
)
import matplotlib.pyplot as plt
from PyQt5.uic import loadUi
 
# Ruta absoluta a la carpeta Vista/ — funciona sin importar desde dónde se corra
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 
class VistaBienvenida(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(BASE_DIR, "Bienvenida.ui"), self)
        self.btnIngresar.clicked.connect(self.ingresar)
 
    def ingresar(self):
        usuario  = self.input_usuario.text()
        password = self.input_password.text()
        rol      = self.combo_rol.currentText()
        self.__controlador.validarLogin(usuario, password, rol)
 
    def setControlador(self, c):
        self.__controlador = c
 
 
class VistaDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(BASE_DIR, "dashboard.ui"), self)
        self.btnDicom.clicked.connect(self.abrirDicom)
        self.btnsenales.clicked.connect(self.abrirSenales)
        self.btnDatos.clicked.connect(self.abrirDatos)
        self.btnSalir.clicked.connect(self.close)
 
    def abrirDicom(self):
        self.__controlador.abrirModuloDicom()
 
    def abrirSenales(self):
        self.__controlador.abrirModuloSenales()
 
    def abrirDatos(self):
        self.__controlador.abrirModuloDatos()
 
    def setControlador(self, c):
        self.__controlador = c
 
 
class VistaDicom(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(BASE_DIR, "dicom.ui"), self)
        self.btnCargarDicom.clicked.connect(self.cargarDicom)
        self.btnConvertirNifti.clicked.connect(self.convertirNifti)
        self.sliderAxial.valueChanged.connect(self.corteAxial)
        self.sliderCoronal.valueChanged.connect(self.corteCoronal)
        self.sliderSagital.valueChanged.connect(self.corteSagital)
 
    def cargarDicom(self):
        self.__controlador.cargarDicom()
 
    def convertirNifti(self):
        self.__controlador.convertirNifti()
 
    def corteAxial(self, valor):
        self.__controlador.mostrarCorteAxial(valor)
 
    def corteCoronal(self, valor):
        self.__controlador.mostrarCorteCoronal(valor)
 
    def corteSagital(self, valor):
        self.__controlador.mostrarCorteSagital(valor)
 
    def setControlador(self, c):
        self.__controlador = c
 
 
class VistaZoom(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(BASE_DIR, "zoom.ui"), self)
        self.btnGuardarZoom.clicked.connect(self.guardarZoom)
 
    def guardarZoom(self):
        nombre = self.txtNombreImagen.text()
        self.__controlador.guardarZoom(nombre)
 
    def setControlador(self, c):
        self.__controlador = c
 
 
class VistaSegmentacion(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(BASE_DIR, "Segmentacion.ui"), self)
        self.btnSegmentar.clicked.connect(self.segmentar)
 
    def segmentar(self):
        metodo = self.cmbThreshold.currentText()
        self.__controlador.segmentar(metodo)
 
    def setControlador(self, c):
        self.__controlador = c
 
 
class VistaMorfologia(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(BASE_DIR, "morfologia.ui"), self)
        self.btnAplicar.clicked.connect(self.aplicar)
 
    def aplicar(self):
        operacion = self.cmbMorfologia.currentText()
        kernel    = self.spinKernel.value()
        self.__controlador.aplicarMorfologia(operacion, kernel)
 
    def setControlador(self, c):
        self.__controlador = c
 
 
class VistaSenales(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(BASE_DIR, "senales.ui"), self)
        self.btnCargarMat.clicked.connect(self.cargarMat)
        self.btnProcesar.clicked.connect(self.procesar)
 
    def cargarMat(self):
        self.__controlador.cargarMat()
 
    def procesar(self):
        self.__controlador.procesar_senal()
 
    def setControlador(self, c):
        self.__controlador = c
 
    def graficar_stem(self, prom_v, des_v):
        fig, ax = plt.subplots()
        ax.stem(prom_v, linefmt='b-', markerfmt='bo', label='Promedio')
        ax.stem(des_v, linefmt='g--', markerfmt='gx', label='Desviación')
        ax.set_title("Promedio y Desviación Estándar")
        ax.legend()
        canvas = FigureCanvas(fig)
        if self.widgetGraficaProcesada.layout() is None:
            layout = QVBoxLayout(self.widgetGraficaProcesada)
            self.widgetGraficaProcesada.setLayout(layout)
        else:
            layout = self.widgetGraficaProcesada.layout()
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)
        layout.addWidget(canvas)
     def canvasoriginal(self, canvas):
        # NOTA: Asegúrate de que en tu archivo "senales.ui" de QtDesigner 
        # el widget blanco para la señal cruda se llame exactamente "widgetGraficaOriginal"
        if self.widgetGraficaOriginal.layout() is None:
            layout = QVBoxLayout(self.widgetGraficaOriginal)
            self.widgetGraficaOriginal.setLayout(layout)
        else:
            layout = self.widgetGraficaOriginal.layout()
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)
        layout.addWidget(canvas)
 
 
class VistaDatos(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(BASE_DIR, "datos.ui"), self)
        self.btnCargarCSV.clicked.connect(self.cargarCSV)
        self.btnCargarExcel.clicked.connect(self.cargarExcel)
        self.btnScatter.clicked.connect(self.scatter)
 
    def cargarCSV(self):
        self.__controlador.cargarCSV()
 
    def cargarExcel(self):
        self.__controlador.cargarExcel()
 
    def scatter(self):
        self.__controlador.graficarScatter()
 
    def setControlador(self, c):
        self.__controlador = c
 
    def mostrarDatos(self, info_df, describe_df):
        self.tablaDatos.setRowCount(describe_df.shape[0])
        self.tablaDatos.setColumnCount(describe_df.shape[1])
        self.tablaDatos.setHorizontalHeaderLabels(describe_df.columns.astype(str).tolist())
        for i in range(describe_df.shape[0]):
            for j in range(describe_df.shape[1]):
                self.tablaDatos.setItem(i, j, QTableWidgetItem(str(describe_df.iloc[i, j])))
 
        self.tablaInfo.setRowCount(info_df.shape[0])
        self.tablaInfo.setColumnCount(info_df.shape[1])
        self.tablaInfo.setHorizontalHeaderLabels(info_df.columns.astype(str).tolist())
        for i in range(info_df.shape[0]):
            for j in range(info_df.shape[1]):
                self.tablaInfo.setItem(i, j, QTableWidgetItem(str(info_df.iloc[i, j])))
 
    def actualizarComboboxes(self, lista_columnas):
        self.cmbX.clear()
        self.cmbY.clear()
        self.cmbX.addItems(lista_columnas)
        self.cmbY.addItems(lista_columnas)
 
    def graficadoraCanvas(self, canvas):
        if self.widget.layout() is not None:
            while self.widget.layout().count():
                item = self.widget.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        else:
            layout_interno = QVBoxLayout(self.widget)
            self.widget.setLayout(layout_interno)
        self.widget.layout().addWidget(canvas)
