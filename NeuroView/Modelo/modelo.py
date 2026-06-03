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
 
        # Liberamos la cámara y cerramos la ventana
        camara.release()
        cv2.destroyAllWindows()
 
        return ruta_guardada 

    # 9, 10, 11 

 
    def cargarCSV(self, ruta):
       
        #Carga un archivo CSV en self.df y retorna la lista de columnas para llenar en la vista.
      
        self.df = pd.read_csv(ruta)
        return self.df.columns.tolist()
 
    def cargarExcel(self, ruta):
        #Carga un archivo Excel en self.df y retorna la lista de columnas.
    
        self.df = pd.read_excel(ruta)
        return self.df.columns.tolist()
 
    def obtenerInfoDescribe(self):
        #Retorna un DataFrame combinado con info() simulado y describe() para mostrarlo en un QTableWidget en la vista.
        if self.df is None:
            return None
 
        # Construimos la tabla de info() manualmente
        info_df = pd.DataFrame({
            "Columna": self.df.columns,
            "Tipo"   : self.df.dtypes.values.astype(str),
            "No nulos": self.df.count().values,
            "Nulos"  : self.df.isnull().sum().values
        })
 
        # describe() trae estadísticas de columnas numéricas
        describe_df = self.df.describe().reset_index()
        describe_df.rename(columns={"index": "Estadístico"}, inplace=True)
 
        return info_df, describe_df
 
    def graficarColumnas(self, columnas):
        #gráfico tipo plot de cada columna de manera individual.
        
        if self.df is None:
            return
 
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
        plt.tight_layout()
        plt.show()
 
    def graficarScatter(self, x, y):
        #Hace un scatter entre la columna x y la columna y del DataFrame.
        if self.df is None:
            return
 
        plt.figure(figsize=(6, 5))
        plt.scatter(self.df[x], self.df[y], alpha=0.6, edgecolors='k', linewidths=0.5)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f"Scatter: {x} vs {y}")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
     
#8.SEÑALES .mat
 
    def cargarMat(self, ruta):
        
        #Carga un archivo .mat y crea un objeto ModeloSenal
        
        self.senalObj = ModeloSenal(ruta)
        return self.senalObj.datos2D.shape  # (canales, muestras)
 
    def procesarCanales(self, inicio, fin):
        #selecciona los canales desde inicio hasta fin de la señal 2D y los grafica en la vista.
        
        if self.senalObj is None:
            return
 
        # Extraemos el rango de canales pedido
        segmento = self.senalObj.datos2D[inicio:fin + 1, :]
 
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
        plt.tight_layout()
        plt.show()
 
    def agregarRuido(self, canal):
        #toma un canal de la señal 2D, le suma ruido gaussiano y muestra en dos subplots la señal original y la modificada.
        
        if self.senalObj is None:
            return
 
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
        plt.tight_layout()
        plt.show()
 
    def estadisticasSenal(self, eje):
        #calcula promedio y desviación estándar a lo largo del eje indicado
        
        if self.senalObj is None:
            return
 
        promedio = np.mean(self.senalObj.datos3D, axis=eje)
        std      = np.std(self.senalObj.datos3D,  axis=eje)
 
        # Si el resultado es multidimensional lo aplanamos para graficar
        promedio = promedio.flatten()
        std      = std.flatten()
 
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
 
        # Stem para promedio
        ax1.stem(promedio, linefmt="C0-", markerfmt="C0o", basefmt="k-")
        ax1.set_title(f"Promedio — eje {eje}")
        ax1.set_xlabel(f"Índice eje {eje}")
        ax1.set_ylabel("Promedio")
        ax1.grid(True)
 
        # Stem para desviación estándar
        ax2.stem(std, linefmt="C1-", markerfmt="C1o", basefmt="k-")
        ax2.set_title(f"Desviación estándar — eje {eje}")
        ax2.set_xlabel(f"Índice eje {eje}")
        ax2.set_ylabel("Std")
        ax2.grid(True)
 
        plt.suptitle(f"Estadísticas sobre eje {eje}", fontsize=12)
        plt.tight_layout()
        plt.show()

# Atributos obligatorios
 
class ModeloSenal:
 
    def __init__(self, ruta):
        #datos3D: matriz original tal como viene del .mat
        #datos2D: señal aplanada a 2 dimensiones (canales x muestras)
    
        mat = sio.loadmat(ruta)
 
        clave = [k for k in mat.keys() if not k.startswith("__")][0]
        datos = mat[clave]
 
        #matriz 3D original
        # Si el archivo viene en 2D lo expandimos a 3D agregando una dimensión
        if datos.ndim == 2:
            self.datos3D = datos[np.newaxis, :, :]  # (1, canales, muestras)
        else:
            self.datos3D = datos  # ya viene en 3D
 
        #  señal reshapeada a 2D 
        # Aplanamos las primeras dimensiones dejando solo (canales, muestras)
        forma = self.datos3D.shape
        self.datos2D = self.datos3D.reshape(-1, forma[-1])
 
