import sqlite3
import os
import datetime
import cv2  
import numpy as np  
import pandas as pd  
import scipy.io as sio
import matplotlib.pyplot as plt

class Modelo:

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "..", "neuroview.db")
        self.conexion = sqlite3.connect(db_path)
        self.cursor = self.conexion.cursor()
        

        # Creamos la tabla de sesiones si no existe
        # Guarda id, ruta de la foto y fecha de la sesión
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sesiones (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario  TEXT,
                ruta     TEXT,
                fecha    TEXT
            )
        """)
        self.conexion.commit()
 
        # Atributo donde guardaremos el DataFrame de datos tabulares
        self.df = None
 
        # Atributo donde guardaremos la señal .mat
        self.senalObj = None
        self.tabularObj = None

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

#OpenCV para capturar por camara
    def capturarFoto(self, usuario):
 
        #Creamos la carpeta fotos si no existe
        base_dir = os.path.dirname(os.path.abspath(__file__))
        carpeta = os.path.join(base_dir, "..", "fotos")
        os.makedirs(carpeta, exist_ok=True)
 
        # Abrimos la cámara (0 = cámara por defecto del computador)
        camara = cv2.VideoCapture(0)
 
        if not camara.isOpened():
            # Si no hay cámara disponible avisamos y salimos
            return None
 
        ruta_guardada = None
 
        while True:
            # Leemos frame a frame
            ret, frame = camara.read()
            if not ret:
                break
 
            # Mostramos el texto de instrucción sobre el video
            cv2.putText(
                frame,
                "Presiona ESPACIO para tomar la foto o ESC para cancelar",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
 
            # Mostramos la ventana de la cámara
            cv2.imshow("Captura de sesion - NeuroView", frame)
 
            tecla = cv2.waitKey(1)
 
            if tecla == 32:  # ESPACIO
                # 1. Calculamos los tiempos primero
                fecha_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                fecha_legible = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                nombre_archivo = f"{usuario}_{fecha_hora}.jpg"
                ruta_guardada = os.path.join(carpeta, nombre_archivo)
 
                # 2. Guardamos físicamente la imagen 
                cv2.imwrite(ruta_guardada, frame)
 
                # 3. Guardamos en la BD de forma segura
                self.cursor.execute(
                    "INSERT INTO sesiones (usuario, ruta, fecha) VALUES (?, ?, ?)",
                    (usuario, ruta_guardada, fecha_legible)
                )
                self.conexion.commit()
                break
 
            elif tecla == 27:  # ESC 
                break
 
        # Liberamos la cámara y cerramos la ventana
        camara.release()
        cv2.destroyAllWindows()
 
        return ruta_guardada
 
        # 9, 10, 11 

 
    def cargarCSV(self, ruta):
        #Carga un archivo CSV en self.df y retorna la lista de columnas para llenar en la vista.
        self.tabularObj = ModeloTabular(ruta)
        self.df = self.tabularObj.df
        return self.df.columns.tolist()
 
    def cargarExcel(self, ruta):
        #Carga un archivo Excel en self.df y retorna la lista de columnas.
        self.tabularObj = ModeloTabular(ruta)
        self.df = self.tabularObj.df
        return self.df.columns.tolist()
 
    def obtenerInfoDescribe(self):
        #Retorna un DataFrame combinado con info() simulado y describe() para mostrarlo en un QTableWidget en la vista.
        if self.tabularObj is None:
            return None
        return self.tabularObj.info_general()
 
    def graficarColumnas(self, columnas):
        #gráfico tipo plot de cada columna de manera individual.
        if self.df is None:
            return None
 
        n = len(columnas)
        fig, axes = plt.subplots(1, n, figsize=(5 * n, 4))
 
        # Si solo hay una columna axes no es lista, lo convertimos
        if n == 1:
            axes = [axes]
 
        for ax, col in zip(axes, columnas):
            ax.plot(self.df[col].values)       # gráfico tipo plot
            ax.set_title(col)
            ax.set_xlabel("Índice")
            ax.set_ylabel(col)
            ax.grid(True)
 
        fig.suptitle("Gráficos individuales por columna", fontsize=13)
        fig.tight_layout()
        return fig
 
    def graficarScatter(self, x, y):
        #Hace un scatter entre la columna x y la columna y del DataFrame.
        if self.df is None:
            return None
        fig, ax = plt.subplots(figsize=(6,5)) # con esto se crea la grafica 
        ax.scatter(self.df[x], self.df[y], alpha=0.6, edgecolors='k', linewidths=0.5)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f"Scatter: {x} vs {y}")
        plt.grid(True)
        plt.tight_layout()
        fig.tight_layout()
        return fig # y aqui se retorna esa al controlodor 
     
#8.SEÑALES .mat
 
    def cargarMat(self, ruta):
        #Carga un archivo .mat y crea un objeto ModeloSenal
        self.senalObj = ModeloSenal(ruta)
        return self.senalObj.datos2D.shape  # se retorna la info al controlador (canales, muestras)
 
    def procesarCanales(self, inicio, fin):
        #selecciona los canales desde inicio hasta fin de la señal 2D y los grafica en la vista.
        if self.senalObj is None:
            return None
 
        # Extraemos el rango de canales pedido
        segmento = self.senalObj.seleccionarCanales(inicio, fin)#aqui se aprovecho la encapsulación ya se creo el metodo seleccionarCanales()
 
        fig, ax = plt.subplots(figsize=(10, 4))
        for i, canal in enumerate(segmento):
            # Desplazamos cada canal verticalmente para que no se encimen
            ax.plot(canal + i * np.max(np.abs(segmento)) * 2,
                    label=f"Canal {inicio + i}")
 
        ax.set_title(f"Canales {inicio} a {fin}")
        ax.set_xlabel("Muestras")
        ax.set_ylabel("Amplitud")
        ax.legend(loc="upper right", fontsize=7)
        ax.grid(True)
        fig.tight_layout()
        return fig
    def GraficaOriginal(self,inicio,fin):
        if self.senalObj is None:
            return None
        segmento = self.senalObj.seleccionarCanales(inicio, fin)
        fig, ax = plt.subplots(figsize=(10, 4))
        for i, canal in enumerate(segmento):
            # Tu misma fórmula matemática de separación para que no se encimen:
            desplazamiento = i * np.max(np.abs(segmento)) * 2
            ax.plot(canal + desplazamiento, label=f"Canal {inicio + i}")

        ax.set_title(f"Señales Originales Crudas — Canales {inicio} a {fin}")
        ax.set_xlabel("Muestras")
        ax.set_ylabel("Amplitud")
        ax.legend(loc="upper right", fontsize=7)
        ax.grid(True)
        
        fig.tight_layout()
        return fig

    def agregarRuido(self, canal):
        #toma un canal de la señal 2D, le suma ruido gaussiano y muestra en dos subplots la señal original y la modificada.
        
        if self.senalObj is None:
            return None
 
        original  = self.senalObj.datos2D[canal, :]
 
        # Generamos ruido gaussiano 
        ruido     = np.random.normal(0, np.std(original) * 0.5, original.shape)
        modificada = original + ruido
 
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
 
        ax1.plot(original, color="steelblue")
        ax1.set_title(f"Canal {canal} — Original")
        ax1.set_ylabel("Amplitud")
        ax1.grid(True)
 
        ax2.plot(modificada, color="tomato")
        ax2.set_title(f"Canal {canal} — Con ruido")
        ax2.set_xlabel("Muestras")
        ax2.set_ylabel("Amplitud")
        ax2.grid(True)
 
        plt.suptitle("Señal original vs señal con ruido", fontsize=12)
        fig.tight_layout()
        return fig
 
    def estadisticasSenal(self, eje):
        if self.senalObj is None:
            return None

        prom, desviacion = self.senalObj.promYdesviacion(eje)

        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,4))

        ax1.stem(prom)
        ax1.set_title("Promedio")
        ax1.set_xlabel("Índice")
        ax1.set_ylabel("Valor")

        ax2.stem(desviacion)
        ax2.set_title("Desviación estándar")
        ax2.set_xlabel("Índice")
        ax2.set_ylabel("Valor")

        fig.tight_layout()

        return fig
    #En esta parte se usa el atributo promYdesviación de la clase ModeloSenal para que cree los graficos stem
    def procesarRuido(self,canal, nivel_ruido):
        return self.senalObj.modificarRuido(canal,nivel_ruido)
# Atributos obligatorios
 
class ModeloSenal:
 
    def __init__(self, ruta):
        #datos3D: matriz original tal como viene del .mat
        #datos2D: señal aplanada a 2 dimensiones (canales x muestras)
        mat = sio.loadmat(ruta)
        #con esta parte el codigo busca la clave del diccionario
        clave = [k for k in mat.keys() if not k.startswith("__")][0]
        datos = mat[clave]
 
        # se almacena la matriz 3D original
        # y sii el archivo viene en 2D lo expandimos a 3D agregando una dimensión
        if datos.ndim == 2:
            self.datos3D = datos[np.newaxis, :, :]  # (1, canales, muestras)
        else:
            self.datos3D = datos  # ya viene en 3D
 
        #  señal reshapeada a 2D 
        # se aplana/modifica las primeras dimensiones dejando solo (canales, muestras)
        forma = self.datos3D.shape
        self.datos2D = self.datos3D.reshape(-1, forma[-1])
    def seleccionarCanales(self, canal_ini, canal_fin):
        #Aqui se trabaja con la señal 2D
        senal_mod =self.datos2D[canal_ini : canal_fin + 1, :]# aqui se sumo 1 al canal final por los limites mmm
        return senal_mod

    def modificarRuido(self,canal,nivel_ruido):
        #con este metodo se trabaja con la señal 2D
        sen_original = self.datos2D[canal,:]
        ruido = np.random.normal(0,nivel_ruido, sen_original.shape)
        new_ruido = sen_original + ruido
        #se retornan para que el controlador las lleve a graficar en los subplots
        return sen_original, new_ruido
    
    def promYdesviacion(self, eje):
        #aqui se debe trabajar con la matriz 3D original
        mat3d= self.datos3D
        prom = np.mean(mat3d, axis=eje)# con la función mean calculamos el promedio del eje que el usuario eligio
        desviacion= np.std(mat3d, axis=eje) #y esta es para la desviación estandar(que tan variados están los datos)
        #aqui se ve la posibilidad que al palicar el mean o std a los ejes
        #el resultado sea una matriz 2D por esta razon se transforma el resultado
        #a un vector si llega a ser necesario
        prom_vector = prom.flatten() #por lo anterior usamos la función flatten :) nos achata la matriz
        desviacion_vector = desviacion.flatten()
        #se retornan los dos vectores 
        return prom_vector, desviacion_vector
class ModeloTabular:
    def __init__(self,ruta):
    #cuando el usuario cargue el archivo la idea es que se guarde como dataframe (por eso aqui usamos pandas)
        self.ruta = ruta      
        _, extension = os.path.splitext(ruta) #en esta parte se guarda el tipo de extensión 
                                              #en la variable para que pandas pueda leer cada formato
        #DataFrame
        if extension.lower() == '.csv':
            self.df = pd.read_csv(ruta)
        elif extension.lower() in ['.xlsx', '.xls']:
            self.df = pd.read_excel(ruta)
        else:
            raise ValueError("Formato de archivo no soportado. Debe ser CSV o Excel.")
    def info_general(self):
        info_df = pd.DataFrame({

            "Columna": self.df.columns, #aqui estan los nombres de las columnas
            "Tipo": self.df.dtypes.astype(str).values, #aqui se convierten los tipos de texto para poderlos pasar al Dataframe
            "No nulos": self.df.count().values, #aqui se cuentan los valores que no son nulos o los espaioc NaN
            "Nulos": self.df.isnull().sum().values})#toda esta info es lo que hace .info() sino que esta función no devuleve en DataFrame por eso se hizo así

        describe_df = self.df.describe().reset_index() # .describe() calcula automáticamente: media, desviación estándar, 
        # mínimos, máximos y percentiles de las columnas numéricas.
        describe_df.rename(columns={"index":"Estadístico"}, inplace=True)
        return info_df, describe_df
    def filtrar_col(self, col1, col2):
        # aqui se reciben los nombres de las columnas elegidas por el usuario
        #y luego se filtra el Dataframe original 
        df_filtrado = self.df[[col1, col2]]
        return df_filtrado
    