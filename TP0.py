"""
TP 0 - Procesamiento Digital de Imágenes (PDI)
==============================================
Aplicación con interfaz gráfica (GUI) desarrollada en Tkinter para realizar 
operaciones básicas de procesamiento de imágenes utilizando la librería NumPy.

Requisitos:
    - tkinter
    - numpy
    - Pillow (PIL)
    - matplotlib
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


class PDIApp:
    """Clase principal que gestiona la interfaz gráfica y la lógica del programa."""

    def __init__(self, root: tk.Tk):
        """Inicializa la ventana principal y los estados de la aplicación.
        
        Args:
            root (tk.Tk): Instancia raíz de Tkinter.
        """
        self.root = root
        self.root.title("TP 0 - Procesamiento Digital de Imágenes")
        self.root.geometry("950x650")

        # --- ESTRUCTURAS DE DATOS ---
        # Representación de imágenes en arreglos de NumPy (matrices uint8)
        self.img_original = None   # Imagen cargada inicialmente (Matriz RGB: Alto x Ancho x 3)
        self.img_entrada = None    # Imagen actual sobre la que se operará
        self.img_resultado = None  # Imagen procesada (Canal RGB 3D o Grises 2D)

        # Referencias a imágenes de Tkinter para evitar que el Garbage Collector las elimine
        self.tk_in = None
        self.tk_out = None

        # Construir elementos visuales
        self._crear_interfaz()

    def _crear_interfaz(self):
        """Construye y organiza todos los widgets de la interfaz gráfica."""
        
        # 1. Panel Superior (Botones de archivo y flujo de trabajo)
        top_frame = tk.Frame(self.root, pady=5)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Button(top_frame, text="Cargar Imagen", command=self.cargar_imagen, bg="#e1e1e1").pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Pasar Resultado a Entrada", command=self.resultado_a_entrada).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Restaurar Original", command=self.restaurar_original).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Guardar PNG", command=self.guardar_resultado, bg="#d1e7dd").pack(side=tk.LEFT, padx=5)

        # 2. Panel Lateral Izquierdo (Operaciones de Procesamiento)
        ops_frame = tk.LabelFrame(self.root, text="Operaciones", padx=10, pady=10)
        ops_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Botones de filtrado de color
        tk.Button(ops_frame, text="Escala de Grises", command=self.convertir_grises, width=18).pack(pady=4)
        tk.Button(ops_frame, text="Canal Rojo", command=lambda: self.aislar_canal(0), width=18, fg="red").pack(pady=4)
        tk.Button(ops_frame, text="Canal Verde", command=lambda: self.aislar_canal(1), width=18, fg="green").pack(pady=4)
        tk.Button(ops_frame, text="Canal Azul", command=lambda: self.aislar_canal(2), width=18, fg="blue").pack(pady=4)

        # Botones de visualización de Histogramas
        tk.Label(ops_frame, text="--- Histograma ---").pack(pady=10)
        tk.Button(ops_frame, text="Ver Hist. Entrada", command=lambda: self.mostrar_histograma(self.img_entrada, "Entrada")).pack(pady=2)
        tk.Button(ops_frame, text="Ver Hist. Resultado", command=lambda: self.mostrar_histograma(self.img_resultado, "Resultado")).pack(pady=2)

        # 3. Panel Central (Visualizadores de Imágenes)
        img_container = tk.Frame(self.root)
        img_container.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        # Visor de la Imagen de Entrada
        frame_in = tk.LabelFrame(img_container, text="Imagen de Entrada")
        frame_in.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        self.lbl_entrada = tk.Label(frame_in, bg="#f0f0f0")
        self.lbl_entrada.pack(expand=True, fill=tk.BOTH)

        # Visor de la Imagen de Resultado
        frame_out = tk.LabelFrame(img_container, text="Imagen Resultado")
        frame_out.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)
        self.lbl_resultado = tk.Label(frame_out, bg="#f0f0f0")
        self.lbl_resultado.pack(expand=True, fill=tk.BOTH)

    def array_to_image_tk(self, arr: np.ndarray) -> ImageTk.PhotoImage:
        """Convierte una matriz NumPy (uint8) a un objeto PhotoImage legible por Tkinter.
        
        Args:
            arr (np.ndarray): Matriz de la imagen en formato NumPy.

        Returns:
            ImageTk.PhotoImage: Imagen escalada lista para desplegar en un Label de Tkinter.
        """
        if arr is None:
            return None
        
        # 1. Crear imagen PIL desde la matriz de NumPy
        img_pil = Image.fromarray(arr)
        
        # 2. Redimensionar preservando el aspecto para encajar en la UI (máx 400x400 px)
        img_pil.thumbnail((400, 400))
        
        # 3. Transformar a formato Tkinter
        return ImageTk.PhotoImage(img_pil)

    def cargar_imagen(self):
        """Abre un cuadro de diálogo para seleccionar una imagen del disco y la carga como matriz NumPy."""
        filepath = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
        if not filepath:
            return  # El usuario canceló la selección

        # Cargar con PIL y forzar a espacio de color RGB de 3 canales
        pil_img = Image.open(filepath).convert("RGB")
        
        # Convertir a matriz NumPy de enteros sin signo de 8 bits (0-255)
        self.img_original = np.array(pil_img, dtype=np.uint8)
        self.img_entrada = self.img_original.copy()
        self.img_resultado = None

        # Refrescar los elementos de la interfaz
        self.actualizar_vistas()

    def actualizar_vistas(self):
        """Actualiza los Labels de Tkinter mostrando el contenido de las matrices de imagen actuales."""
        # Actualizar vista de Entrada
        if self.img_entrada is not None:
            self.tk_in = self.array_to_image_tk(self.img_entrada)
            self.lbl_entrada.config(image=self.tk_in)
        else:
            self.lbl_entrada.config(image="")

        # Actualizar vista de Resultado
        if self.img_resultado is not None:
            self.tk_out = self.array_to_image_tk(self.img_resultado)
            self.lbl_resultado.config(image=self.tk_out)
        else:
            self.lbl_resultado.config(image="")

    # =========================================================================
    # LÓGICA DE PROCESAMIENTO DIGITAL DE IMÁGENES (NumPy)
    # =========================================================================

    def convertir_grises(self):
        """Convierte la imagen de entrada a escala de grises mediante el producto escalar
        utilizando los pesos de luminancia estándar NTSC (0.299*R + 0.587*G + 0.114*B).
        """
        if self.img_entrada is None:
            return
        
        pesos = np.array([0.299, 0.587, 0.114])
        
        # Realizar el producto punto entre la dimensión de canales (RGB) y los pesos NTSC
        grises = np.dot(self.img_entrada[..., :3], pesos).astype(np.uint8)
        
        self.img_resultado = grises
        self.actualizar_vistas()

    def aislar_canal(self, canal_idx: int):
        """Aísla un canal de color específico anulando los otros dos.
        
        Args:
            canal_idx (int): 0 para Rojo (R), 1 para Verde (G), 2 para Azul (B).
        """
        if self.img_entrada is None:
            return
        
        # Crear una matriz de ceros de la misma forma y tipo que la de entrada
        res = np.zeros_like(self.img_entrada)
        
        # Copiar únicamente los datos del canal deseado
        res[..., canal_idx] = self.img_entrada[..., canal_idx]
        
        self.img_resultado = res
        self.actualizar_vistas()

    # =========================================================================
    # GESTIÓN DEL FLUJO DE TRABAJO
    # =========================================================================

    def resultado_a_entrada(self):
        """Copia la imagen de resultado actual al panel de entrada para permitir
        el encadenamiento de múltiples operaciones.
        """
        if self.img_resultado is None:
            messagebox.showwarning("Advertencia", "No hay una imagen resultado para transferir.")
            return

        # Si la imagen resultado es bidimensional (escala de grises), adaptar a matriz 3D RGB
        if self.img_resultado.ndim == 2:
            self.img_entrada = np.stack((self.img_resultado,) * 3, axis=-1)
        else:
            self.img_entrada = self.img_resultado.copy()

        self.img_resultado = None
        self.actualizar_vistas()

    def restaurar_original(self):
        """Descarta las modificaciones y vuelve a colocar la imagen cargada originalmente en la entrada."""
        if self.img_original is None:
            return
        self.img_entrada = self.img_original.copy()
        self.img_resultado = None
        self.actualizar_vistas()

    def guardar_resultado(self):
        """Guarda la imagen resultado procesada actualmente en el almacenamiento local (formato PNG)."""
        if self.img_resultado is None:
            messagebox.showwarning("Advertencia", "No hay ninguna imagen resultado para guardar.")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if filepath:
            img_pil = Image.fromarray(self.img_resultado)
            img_pil.save(filepath)
            messagebox.showinfo("Éxito", f"Imagen guardada en:\n{filepath}")

    # =========================================================================
    # CÁLCULO Y GRÁFICO DE HISTOGRAMAS (Matplotlib & NumPy)
    # =========================================================================

    def mostrar_histograma(self, img_array: np.ndarray, titulo: str):
        """Calcula y grafica el histograma de frecuencias de intensidad (0-255)
        utilizando NumPy para el cálculo de rangos y Matplotlib para el renderizado.

        Args:
            img_array (np.ndarray): Matriz de datos de la imagen a analizar.
            titulo (str): Identificador para la ventana ("Entrada" o "Resultado").
        """
        if img_array is None:
            messagebox.showwarning("Advertencia", f"No hay imagen de {titulo.lower()} para calcular el histograma.")
            return

        # Crear figura independiente con Matplotlib
        plt.figure(f"Histograma - {titulo}")
        plt.title(f"Histograma de Intensidades ({titulo})")
        plt.xlabel("Intensidad de Píxel (0 - 255)")
        plt.ylabel("Frecuencia (Nº de Píxeles)")

        # Histograma para imagen mono-canal (Escala de Grises)
        if img_array.ndim == 2:
            hist, _ = np.histogram(img_array, bins=256, range=(0, 256))
            plt.plot(hist, color='black', label='Grises')
            
        # Histograma tri-canal (RGB)
        else:
            colores = ('red', 'green', 'blue')
            for i, col in enumerate(colores):
                # Calcular la distribución por cada uno de los 3 canales individualmente
                hist, _ = np.histogram(img_array[..., i], bins=256, range=(0, 256))
                plt.plot(hist, color=col, label=f'Canal {col.capitalize()}')

        # Ajustar límites y mostrar el gráfico
        plt.xlim([0, 256])
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()


# Punto de entrada de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = PDIApp(root)
    root.mainloop()