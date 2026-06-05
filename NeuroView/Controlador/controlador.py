
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
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self.__vistaSenales, "Seleccionar Archivo de Señal", "", "Archivos MAT (*.mat)")
        if ruta_archivo:
            try:
                # 2. Llamamos al método de tu modelo que procesa las dimensiones
                dimensiones_2d = self.__modelo.cargarMat(ruta_archivo) # Retorna (canales, muestras)
                # 3. Notificamos a la vista que el archivo cargó con éxito
                # (Opcional: Podrías usar esto para configurar los rangos de tus SpinBox o sliders en la UI)
                QMessageBox.information(
                    self.__vistaSenales, "Éxito", 
                    f"Señal cargada correctamente.\nDimensiones de análisis 2D: {dimensiones_2d}")
            except Exception as e:
                QMessageBox.critical(self.__vistaSenales, "Error", f"No se pudo cargar el archivo .mat: {str(e)}")

    def procesarSenales(self, inicio, fin, tiempo_inicio, tiempo_fin):
        try:
            # 1. Le pedimos la figura procesada al modelo (con la corrección sin plt.show)
            figura = self.__modelo.procesarCanales(inicio, fin, tiempo_inicio, tiempo_fin)
            
            if figura is None:
                QMessageBox.warning(self.__vistaSenales, "Atención", "Primero debes cargar un archivo .mat")
                return
            # 2. Convertimos la figura de Matplotlib en un Widget compatible con PyQt
            canvas = FigureCanvas(figura)
            
            # 3. Limpiamos y pintamos sobre el contenedor asignado en tu VistaSenales
            # Asumiendo que en tu archivo VistaSenales creaste un método para renderizar el lienzo
            self.__vistaSenales.mostrarGraficoEnLayout(canvas)
            
        except Exception as e:
            QMessageBox.critical(self.__vistaSenales, "Error de Procesamiento", str(e))

    # datos tabulares

    def cargarCSV(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self.__vistaDatos, "Seleccionar Archivo CSV", "", "Archivos CSV (*.csv)"
        )
        if ruta_archivo:
            try:
                # El modelo carga los datos y nos devuelve la lista con los nombres de las columnas
                columnas = self.__modelo.cargarCSV(ruta_archivo)
                
                # Le pedimos al modelo los DataFrames estadísticos calculados
                info_df, describe_df = self.__modelo.obtenerInfoDescribe()
                
                # Le ordenamos a la vista actualizar sus tablas visuales y cargar los ComboBox
                self.__vistaDatos.actualizarComboColumnas(columnas)
                self.__vistaDatos.mostrarEstadisticasTablas(info_df, describe_df)
                
            except Exception as e:
                QMessageBox.critical(self.__vistaDatos, "Error", f"Error al procesar el CSV: {str(e)}")

    def cargarExcel(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self.__vistaDatos, "Seleccionar Archivo Excel", "", "Archivos Excel (*.xlsx *.xls)"
        )
        if ruta_archivo:
            try:
                columnas = self.__modelo.cargarExcel(ruta_archivo)
                info_df, describe_df = self.__modelo.obtenerInfoDescribe()
                
                self.__vistaDatos.actualizarComboColumnas(columnas)
                self.__vistaDatos.mostrarEstadisticasTablas(info_df, describe_df)
            except Exception as e:
                QMessageBox.critical(self.__vistaDatos, "Error", f"Error al procesar el Excel: {str(e)}")

    def graficarScatter(self, x, y):
        # Este método se ejecutará cuando el usuario presione el botón "Graficar Scatter"
        if not x or not y:
            QMessageBox.warning(self.__vistaDatos, "Atención", "Debes seleccionar dos columnas válidas.")
            return
            
        figura = self.__modelo.graficarScatter(x, y)
        if figura is None:
            QMessageBox.warning(self.__vistaDatos, "Atención", "No hay datos cargados para graficar.")
            return
            
        # Convertimos a canvas e insertamos nativamente en la UI sin ventanas externas flotantes
        canvas = FigureCanvas(figura)
        self.__vistaDatos.mostrarScatterEnLayout(canvas)