
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog, QVBoxLayout, QTableWidgetItem
)
import matplotlib.pyplot as plt
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

        self.btnCargarMat.clicked.connect(self.cargarMat)
        self.btnProcesar.clicked.connect(self.procesar)

    def cargarMat(self):
        self.__controlador.cargarMat()

    def procesar(self):
        #aqui la vista le indica al controlador que el usuario seleccionó procesar
        #entonces el controlador se encarga de leer y devolver la señal procesada
        self.__controlador.procesar_senal()

    def setControlador(self, c):
        self.__controlador = c
# El usuario carga un CSV o Excel con datos medicos,
# ve la info/describe del archivo, hace plots y scatter.

class VistaDatos(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi("Vista/datos.ui", self)
        
        self.btnCargarCSV.clicked.connect(self.cargarCSV)
        self.btnCargarExcel.clicked.connect(self.cargarExcel)
        self.btnScatter.clicked.connect(self.scatter)
    #esta parte es para conectar los botenes y cargar la vista de de datos.iu
    def cargarCSV(self):
        self.__controlador.cargarCSV()

    def cargarExcel(self):
        self.__controlador.cargarExcel()

    def scatter(self):
        # Leemos las dos columnas elegidas por el usuario en los combos
        self.__controlador.graficarScatter()

    def setControlador(self, c):
        self.__controlador = c

    def mostrarDatos(self,info_df, describe_df):
    #para la tabla de estaditicas
        self.tablaDatos.setRowCount(describe_df.shape[0])
        self.tablaDatos.setColumnCount(describe_df.shape[1])
        self.tablaDatos.setHorizontalHeaderLabels(describe_df.columns.astype(str).tolist())
        
        for i in range(describe_df.shape[0]):
            for j in range(describe_df.shape[1]):
                self.tablaDatos.setItem(i, j, QTableWidgetItem(str(describe_df.iloc[i, j])))   
    #para la tabla de indormación osea todo lo del .info()
        self.tablaDatos_2.setRowCount(info_df.shape[0])
        self.tablaDatos_2.setColumnCount(info_df.shape[1])
        self.tablaDatos_2.setHorizontalHeaderLabels(info_df.columns.astype(str).tolist())

        for i in range(info_df.shape[0]):
            for j in range(info_df.shape[1]):
                self.tablaDatos_2.setItem(i,j,QTableWidgetItem(str(info_df.iloc[i, j])))
                
    def actualizarComboboxes(self, lista_columnas):
        self.cmbX.clear()
        self.cmbY.clear()
        self.cmbX.addItems(lista_columnas)
        self.cmbY.addItems(lista_columnas)

    def graficar_stem(self, prom_v, des_v):
        fig, ax = plt.subplots()
        
        # 2. Dibujamos con la función .stem() que nos pide el requerimiento
        ax.stem(prom_v, linefmt='b-', markerfmt='bo', label='Promedio')
        ax.stem(des_v, linefmt='g--', markerfmt='gx', label='Desviación')
        ax.set_title("Promedio y Desviación Estándar")
        ax.legend()  # Muestra el cuadrito de etiquetas

        # 3. Ponemos el dibujo en el "marco" de PyQt (Canvas)
        canvas = FigureCanvas(fig)

        # 4. Buscamos el contenedor gris de tu imagen (widgetGraficaProcesada)
        # Si no tiene layout, se lo creamos en vertical
        if self.widgetGraficaProcesada.layout() is None:
            from PyQt5.QtWidgets import QVBoxLayout
            layout = QVBoxLayout(self.widgetGraficaProcesada)
            self.widgetGraficaProcesada.setLayout(layout)
        else:
            layout = self.widgetGraficaProcesada.layout()
            # Borramos el gráfico que se haya pintado antes para que no se superpongan
            for i in reversed(range(layout.count())): 
                layout.itemAt(i).widget().setParent(None)

        # 5. ¡Listo! Añadimos el gráfico al espacio de la pantalla
        layout.addWidget(canvas)
        
    def graficadoraCanvas(self,canvas):
        # aqui si limpian los graficos si ya existen para que no se superpongan
        if self.widget.layout() is not None:
            # Esta línea borra limpiamente el gráfico anterior de la pantalla
            while self.widget.layout().count():
                item = self.widget.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        else:
            # Si es la primera vez que graficamos, le creamos un contenedor interno (Layout)
            layout_interno = QVBoxLayout(self.widget)
            self.widget.setLayout(layout_interno)
        
        # Metemos el lienzo (canvas) que nos pasaron dentro de nuestro 'widget'
        self.widget.layout().addWidget(canvas)# con esta parte se evita que salgan ventanas emergentes plt.show()
