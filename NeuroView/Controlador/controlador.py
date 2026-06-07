
# El controlador es el intermediario entre la Vista y el Modelo.
# La vista le dice "el usuario hizo clic en X"
# y el controlador decide que hacer: llama al modelo,
# procesa la respuesta y le dice a la vista que mostrar.
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas #importación adicional para usar la función canvas :)
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem
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
        if self.__vistaSenales is None:
            self.__vistaSenales = VistaSenales()
            self.__vistaSenales.setControlador(self)
        self.__vistaSenales.show()

    def abrirModuloDatos(self):
        if self.__vistaDatos is None:
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
        if self.__vistaSenales is None:
            return
        ruta, _ = QFileDialog.getOpenFileName(self.__vistaSenales, "Seleccionar Archivo de Señal", "", "Archivos MAT (*.mat)")
        if ruta:  
            # Llamamos al metodo de la clase modelo
            forma_2d = self.__modelo.cargarMat(ruta)
            print(f"Archivo cargado\nDimensiones 2D: {forma_2d}")
    def procesar_senal(self):
        # en este punto nos ayudamos para verificar que el usuario si seleccionó el RadioButton de ejes
        if self.__vistaSenales.radioEje0.isChecked() or self.__vistaSenales.radioEje1.isChecked() or self.__vistaSenales.radioEje2.isChecked():
            
            # aqui se revisa cuál de los tres ejes seleccionó
            if self.__vistaSenales.radioEje0.isChecked():
                eje_elegido = 0
            elif self.__vistaSenales.radioEje1.isChecked():
                eje_elegido = 1
            else:
                eje_elegido = 2
            #luego se llama al metodo promYdesviación
            prom_v, des_v = self.__modelo.senalObj.promYdesviación(eje_elegido)
            print("Los promedios y desviaciones estan listos para graficar con stem.")
            # Aquí se llama a la función de la vista para graficar prom_v y des_v con stem
            self.__vistaSenales.graficar_stem(prom_v, des_v)
        # si el usuario no selecciona ejes, se verifica entonces si quiere seleccionar canales
        elif self.__vistaSenales.spinCanalInicial.value() != self.__vistaSenales.spinCanalFinal.value():
            
            # Leemos los valores que el usuario puso en los QSpinBox de tu imagen
            canal_i = self.__vistaSenales.spinCanalInicial.value()
            canal_f = self.__vistaSenales.spinCanalFinal.value()
            #luego se llama al metodo de seleccionarcanales
            senal_recortada = self.__modelo.senalObj.seleccionarCanales(canal_i, canal_f)
            print(f"Canales recortados desde {canal_i} hasta {canal_f}.")
            
        # aqui se modifica el ruido si el usuario no selecciona ninguna de las anteriores
        else:
            canal_ruido = self.__vistaSenales.spinCanalInicial.value() 
            nivel = 0.2 
            # se llama al metodo modificarRuido
            original, ruidosa = self.__modelo.senalObj.modificarRuido(canal_ruido, nivel)
            print("Señal original y con ruido generadas.")
     
    # datos tabulares

    def cargarCSV(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(self.__vistaDatos, "Seleccionar Archivo CSV", "", "Archivos CSV (*.csv)")
        if ruta_archivo:
            try:
                # El modelo carga los datos y nos devuelve la lista con los nombres de las columnas
                columnas = self.__modelo.cargarCSV(ruta_archivo)
                
                # Le pedimos al modelo los DataFrames estadísticos calculados
                info_df, describe_df = self.__modelo.obtenerInfoDescribe()
                
                # Le ordenamos a la vista actualizar sus tablas visuales y cargar los ComboBox
                self.__vistaDatos.actualizarComboboxes(columnas)
                self.__vistaDatos.mostrarDatos(info_df, describe_df)
                
            except Exception as e:
                QMessageBox.critical(self.__vistaDatos, "Error", f"Error al procesar el CSV: {str(e)}")

    def cargarExcel(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(self.__vistaDatos, "Seleccionar Archivo Excel", "", "Archivos Excel (*.xlsx *.xls)")
        if ruta_archivo:
            try:
                columnas = self.__modelo.cargarExcel(ruta_archivo)
                info_df, describe_df = self.__modelo.obtenerInfoDescribe()
                self.__vistaDatos.actualizarComboboxes(columnas)
                self.__vistaDatos.mostrarDatos(info_df, describe_df)
            except Exception as e:
                QMessageBox.critical(self.__vistaDatos, "Error", f"Error al procesar el Excel: {str(e)}")

    def graficarScatter(self, x, y):
        x = self.__vistaDatos.cmbX.currentText()
        y = self.__vistaDatos.cmbY.currentText()
        figura = self.__modelo.graficarScatter(x, y)
        if figura:
            canvas = FigureCanvas(figura)
            self.__vistaDatos.graficadoraCanvas(canvas)
        #FigureCanvas  es una función de matplotlib, 
        #la verdad es muy util ya que toma la figura de matplotlib y la transforma en un widget de pyQt, 
        #en otras palabras es como si rellenara el marco blanco de QTdesigner (hay que hacer una importacion para usarla)
    
    def cargarTabulares(self):
        # esta parte asegura que la ventana de datos esté activa
        if self.__vistaDatos is None:
            return 
        ruta, _ = QFileDialog.getOpenFileName(self.__vistaDatos, "Seleccionar Datos Tabulares", "", "Archivos (*.csv *.xlsx *.xls)")
        if ruta:
            _, extension = os.path.splitext(ruta)
            
            # El modelo carga el archivo y crea internamente el 'tabularObj'
            if extension.lower() == '.csv':
                self.__modelo.cargarCSV(ruta) 
            elif extension.lower() in ['.xlsx', '.xls']:
                self.__modelo.cargarExcel(ruta)
            else:
                print("Formato no compatible.")
                return

            info_tabla, estadisticas_tabla = self.__modelo.tabularObj.info_general()
            
            # se extraen las columnas,como info_tabla es un DataFrame,
            # extraemos los nombres directamente de ahí y se convierten a una lista de Python.
            lista_cols = info_tabla["Columna"].tolist()            
            # se limpian y se listan los 4 ComboBox de la interfaz
            self.__vistaDatos.combo_col1.clear()
            self.__vistaDatos.combo_col2.clear()
            self.__vistaDatos.combo_col3.clear()
            self.__vistaDatos.combo_col4.clear()
            
            self.__vistaDatos.combo_col1.addItems(lista_cols)
            self.__vistaDatos.combo_col2.addItems(lista_cols)
            self.__vistaDatos.combo_col3.addItems(lista_cols)
            self.__vistaDatos.combo_col4.addItems(lista_cols)
            
            # se passan los Dataframes a la vista para graficar las tablas de estadisticas
            self.__vistaDatos.mostrarEstadisticasTablas(info_tabla, estadisticas_tabla)
            
            print(f"Archivo cargado correctamente. Tablas estadísticas y ComboBox actualizados.") 
    def procesarFiltro_tabla(self):
        if self.__vistaDatos is None or not hasattr(self.__modelo, 'tabularObj') or self.__modelo.tabularObj is None:
            return
            
        # se lee los combos() de la vista datos
        c1 = self.__vistaDatos.combo_col1.currentText()
        c2 = self.__vistaDatos.combo_col2.currentText()
        c3 = self.__vistaDatos.combo_col3.currentText()
        c4 = self.__vistaDatos.combo_col4.currentText()
        
        df_recortado = self.__modelo.tabularObj.filtrar_col(c1, c2, c3, c4)
        #resultados en la tabla de la vista de datos
        self.interfazdf(df_recortado)

    def interfazdf(self, dataframe):
        tabla = self.__vistaDatos.tabla_resultados
        tabla.setRowCount(dataframe.shape[0])
        tabla.setColumnCount(dataframe.shape[1])
        tabla.setHorizontalHeaderLabels(dataframe.columns)
        
        for i in range(dataframe.shape[0]):
            for j in range(dataframe.shape[1]):
                valor = str(dataframe.iloc[i, j])
                tabla.setItem(i, j, QTableWidgetItem(valor))