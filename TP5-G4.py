import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.image as mpimg
import imageio

class AplicacionMorfologiaPDI:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("PDI - Morfología y Binarización")
        self.ventana_principal.geometry("1050x750")
        self.ventana_principal.config(bg="#f0f0f0")

        # Variables de almacenamiento de imágenes
        self.ruta_archivo_actual = None
        self.matriz_imagen_original = None
        self.matriz_imagen_procesada = None

        # Creación de la interfaz gráfica
        self.inicializar_interfaz()

    def inicializar_interfaz(self):
        # Título superior
        etiqueta_titulo = tk.Label(
            self.ventana_principal, 
            text="Procesamiento Digital de Imágenes - Morfología y Binarización", 
            font=("Arial", 16, "bold"), 
            bg="#f0f0f0", 
            fg="#333333"
        )
        etiqueta_titulo.pack(pady=10)

        # Contenedor principal de controles
        panel_controles = tk.Frame(self.ventana_principal, bg="#f0f0f0")
        panel_controles.pack(pady=5)

        # Botones de carga y gestión secuencial
        btn_cargar = tk.Button(panel_controles, text="Cargar Imagen", command=self.cargar_imagen, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        btn_cargar.grid(row=0, column=0, padx=5, pady=5)

        btn_copiar = tk.Button(panel_controles, text="Copiar Procesada a Original (Secuencial)", command=self.copiar_procesada_a_original, bg="#FF9800", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        btn_copiar.grid(row=0, column=1, padx=5, pady=5)

        # Contenedor de Binarización
        panel_binarizacion = tk.LabelFrame(self.ventana_principal, text=" Binarización (Valores 0 y 1 / Blanco y Negro) ", font=("Arial", 11, "bold"), bg="#f0f0f0", padx=10, pady=10)
        panel_binarizacion.pack(pady=5, fill="x", padx=20)

        lbl_umbral = tk.Label(panel_binarizacion, text="Umbral (Threshold):", bg="#f0f0f0", font=("Arial", 10))
        lbl_umbral.grid(row=0, column=0, padx=5, sticky="w")

        self.slider_umbral = tk.Scale(panel_binarizacion, from_=0, to=255, orient="horizontal", length=200, bg="#f0f0f0")
        self.slider_umbral.set(128)  # Valor por defecto a la mitad
        self.slider_umbral.grid(row=0, column=1, padx=5)

        btn_binarizar = tk.Button(panel_binarizacion, text="Aplicar Binarización", command=self.ejecutar_binarizacion, bg="#9C27B0", fg="white", font=("Arial", 10, "bold"), padx=10)
        btn_binarizar.grid(row=0, column=2, padx=15)

        # Contenedor de operaciones morfológicas
        panel_operaciones = tk.LabelFrame(self.ventana_principal, text=" Operaciones Morfológicas (Elemento Estructurante 3x3) ", font=("Arial", 11, "bold"), bg="#f0f0f0", padx=10, pady=10)
        panel_operaciones.pack(pady=10, fill="x", padx=20)

        btn_erosion = tk.Button(panel_operaciones, text="Erosión", command=self.ejecutar_erosion, width=15, bg="#2196F3", fg="white", font=("Arial", 10))
        btn_erosion.grid(row=0, column=0, padx=8, pady=5)

        btn_dilatacion = tk.Button(panel_operaciones, text="Dilatación", command=self.ejecutar_dilatacion, width=15, bg="#2196F3", fg="white", font=("Arial", 10))
        btn_dilatacion.grid(row=0, column=1, padx=8, pady=5)

        btn_apertura = tk.Button(panel_operaciones, text="Apertura", command=self.ejecutar_apertura, width=15, bg="#2196F3", fg="white", font=("Arial", 10))
        btn_apertura.grid(row=0, column=2, padx=8, pady=5)

        btn_cierre = tk.Button(panel_operaciones, text="Cierre", command=self.ejecutar_cierre, width=15, bg="#2196F3", fg="white", font=("Arial", 10))
        btn_cierre.grid(row=0, column=3, padx=8, pady=5)

        btn_borde = tk.Button(panel_operaciones, text="Borde Morfológico", command=self.ejecutar_borde, width=15, bg="#2196F3", fg="white", font=("Arial", 10))
        btn_borde.grid(row=1, column=0, padx=8, pady=5, columnspan=2, sticky="ew")

        btn_mediana = tk.Button(panel_operaciones, text="Filtro Mediana", command=self.ejecutar_mediana, width=15, bg="#2196F3", fg="white", font=("Arial", 10))
        btn_mediana.grid(row=1, column=2, padx=8, pady=5, columnspan=2, sticky="ew")

        # Contenedor para visualización de imágenes
        panel_visualizacion = tk.Frame(self.ventana_principal, bg="#f0f0f0")
        panel_visualizacion.pack(pady=10, fill="both", expand=True, padx=20)

        # Panel imagen original
        frame_original = tk.LabelFrame(panel_visualizacion, text="Imagen Original", font=("Arial", 10, "bold"), bg="#f0f0f0")
        frame_original.pack(side="left", expand=True, padx=10)
        self.etiqueta_imagen_original = tk.Label(frame_original, bg="#dddddd")
        self.etiqueta_imagen_original.pack(padx=10, pady=10)

        # Panel imagen procesada
        frame_procesada = tk.LabelFrame(panel_visualizacion, text="Imagen Procesada", font=("Arial", 10, "bold"), bg="#f0f0f0")
        frame_procesada.pack(side="right", expand=True, padx=10)
        self.etiqueta_imagen_procesada = tk.Label(frame_procesada, bg="#dddddd")
        self.etiqueta_imagen_procesada.pack(padx=10, pady=10)

    def cargar_imagen(self):
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp;*.tif")]
        )
        if ruta_archivo:
            self.ruta_archivo_actual = ruta_archivo
            imagen_pil = Image.open(self.ruta_archivo_actual).convert("L")
            self.matriz_imagen_original = np.array(imagen_pil, dtype=np.uint8)
            self.matriz_imagen_procesada = self.matriz_imagen_original.copy()
            
            self.actualizar_visualizacion()

    def actualizar_visualizacion(self):
        if self.matriz_imagen_original is not None:
            img_orig_pil = Image.fromarray(self.matriz_imagen_original)
            img_orig_pil = img_orig_pil.resize((280, 280))
            self.imagen_Tk_original = ImageTk.PhotoImage(img_orig_pil)
            self.etiqueta_imagen_original.config(image=self.imagen_Tk_original)

        if self.matriz_imagen_procesada is not None:
            # Si la matriz maneja valores binarios puros (0 y 1), los escalamos a (0 y 255) para que PIL los pueda visualizar correctamente en pantalla
            matriz_visualizacion = self.matriz_imagen_procesada
            if set(np.unique(matriz_visualizacion)).issubset({0, 1}):
                matriz_visualizacion = matriz_visualizacion * 255

            img_proc_pil = Image.fromarray(matriz_visualizacion.astype(np.uint8))
            img_proc_pil = img_proc_pil.resize((280, 280))
            self.imagen_Tk_procesada = ImageTk.PhotoImage(img_proc_pil)
            self.etiqueta_imagen_procesada.config(image=self.imagen_Tk_procesada)

    def copiar_procesada_a_original(self):
        if self.matriz_imagen_procesada is not None:
            self.matriz_imagen_original = self.matriz_imagen_procesada.copy()
            self.actualizar_visualizacion()
            messagebox.showinfo("Secuencia", "La imagen procesada se ha copiado exitosamente a la original[cite: 1].")
        else:
            messagebox.showwarning("Advertencia", "No hay ninguna imagen procesada para copiar.")

    # ----------------------------------------------------
    # ALGORITMO DE BINARIZACIÓN
    # ----------------------------------------------------
    def calcular_binarizacion(self, matriz_entrada, umbral):
        # Convierte la imagen a valores estrictamente 0 y 1 basados en el umbral
        matriz_resultado = (matriz_entrada > umbral).astype(np.uint8)
        return matriz_resultado

    # ----------------------------------------------------
    # ALGORITMOS DE MORFOLOGÍA MATEMÁTICA (Vecindad 3x3)
    # ----------------------------------------------------
    
    def calcular_erosion_matriz(self, matriz_entrada):
        alto, ancho = matriz_entrada.shape
        matriz_con_padding = np.pad(matriz_entrada, pad_width=1, mode='edge')
        matriz_resultado = np.zeros_like(matriz_entrada)
        
        for i in range(alto):
            for j in range(ancho):
                vecindad_3x3 = matriz_con_padding[i:i+3, j:j+3]
                matriz_resultado[i, j] = np.min(vecindad_3x3) # Mínimo[cite: 1]
        return matriz_resultado

    def calcular_dilatacion_matriz(self, matriz_entrada):
        alto, ancho = matriz_entrada.shape
        matriz_con_padding = np.pad(matriz_entrada, pad_width=1, mode='edge')
        matriz_resultado = np.zeros_like(matriz_entrada)
        
        for i in range(alto):
            for j in range(ancho):
                vecindad_3x3 = matriz_con_padding[i:i+3, j:j+3]
                matriz_resultado[i, j] = np.max(vecindad_3x3) # Máximo[cite: 1]
        return matriz_resultado

    def calcular_mediana_matriz(self, matriz_entrada):
        alto, ancho = matriz_entrada.shape
        matriz_con_padding = np.pad(matriz_entrada, pad_width=1, mode='edge')
        matriz_resultado = np.zeros_like(matriz_entrada)
        
        for i in range(alto):
            for j in range(ancho):
                vecindad_3x3 = matriz_con_padding[i:i+3, j:j+3]
                matriz_resultado[i, j] = np.median(vecindad_3x3) # Mediana[cite: 1]
        return matriz_resultado.astype(np.uint8)

    # ----------------------------------------------------
    # MÉTODOS DE CONTROL PARA LOS BOTONES
    # ----------------------------------------------------

    def ejecutar_binarizacion(self):
        if self.matriz_imagen_original is not None:
            valor_umbral = self.slider_umbral.get()
            self.matriz_imagen_procesada = self.calcular_binarizacion(self.matriz_imagen_original, valor_umbral)
            self.actualizar_visualizacion()

    def ejecutar_erosion(self):
        if self.matriz_imagen_original is not None:
            self.matriz_imagen_procesada = self.calcular_erosion_matriz(self.matriz_imagen_original)
            self.actualizar_visualizacion()

    def ejecutar_dilatacion(self):
        if self.matriz_imagen_original is not None:
            self.matriz_imagen_procesada = self.calcular_dilatacion_matriz(self.matriz_imagen_original)
            self.actualizar_visualizacion()

    def ejecutar_apertura(self):
        if self.matriz_imagen_original is not None:
            imagen_erosionada = self.calcular_erosion_matriz(self.matriz_imagen_original)
            self.matriz_imagen_procesada = self.calcular_dilatacion_matriz(imagen_erosionada)
            self.actualizar_visualizacion()

    def ejecutar_cierre(self):
        if self.matriz_imagen_original is not None:
            imagen_dilatada = self.calcular_dilatacion_matriz(self.matriz_imagen_original)
            self.matriz_imagen_procesada = self.calcular_erosion_matriz(imagen_dilatada)
            self.actualizar_visualizacion()

    def ejecutar_borde(self):
        if self.matriz_imagen_original is not None:
            dilatada = self.calcular_dilatacion_matriz(self.matriz_imagen_original)
            erosionada = self.calcular_erosion_matriz(self.matriz_imagen_original)
            borde = np.clip(dilatada.astype(np.int16) - erosionada.astype(np.int16), 0, 255)
            self.matriz_imagen_procesada = borde.astype(np.uint8)
            self.actualizar_visualizacion()

    def ejecutar_mediana(self):
        if self.matriz_imagen_original is not None:
            self.matriz_imagen_procesada = self.calcular_mediana_matriz(self.matriz_imagen_original)
            self.actualizar_visualizacion()

if __name__ == "__main__":
    ventana_raiz = tk.Tk()
    app = AplicacionMorfologiaPDI(ventana_raiz)
    ventana_raiz.mainloop()