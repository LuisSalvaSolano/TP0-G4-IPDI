# TP 0 – Procesamiento Digital de Imágenes (PDI)

Aplicación de escritorio con interfaz gráfica (Tkinter) para aplicar operaciones básicas de Procesamiento Digital de Imágenes sobre una imagen, usando **NumPy** para el cómputo, **Pillow** para la lectura/escritura de archivos y **Matplotlib** para graficar histogramas.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-informational)
![License](https://img.shields.io/badge/license-MIT-green)

## Contenido

- [Objetivo](#objetivo)
- [Funcionalidades](#funcionalidades)
- [Capturas](#capturas)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Cómo funciona](#cómo-funciona)
- [Cómo agregar nuevas operaciones](#cómo-agregar-nuevas-operaciones)
- [Limitaciones conocidas](#limitaciones-conocidas)
- [Licencia](#licencia)

## Objetivo

La aplicación permite cargar una imagen, aplicarle transformaciones simples (escala de grises, aislamiento de canales RGB) y comparar visualmente la imagen de **entrada** contra el **resultado** procesado, en dos paneles lado a lado. También permite visualizar el histograma de intensidades de cualquiera de los dos paneles.

## Funcionalidades

- 📂 **Cargar imagen** desde el disco (`.png`, `.jpg`, `.jpeg`).
- 🖼️ **Dos paneles independientes**: imagen de entrada e imagen resultado, para comparar antes/después.
- ⚙️ **Operaciones de procesamiento**:
  - Conversión a escala de grises (ponderación NTSC: `0.299·R + 0.587·G + 0.114·B`).
  - Aislamiento de canal Rojo, Verde o Azul.
- 🔁 **Encadenar operaciones**: botón para pasar el resultado al panel de entrada y seguir procesando.
- ↩️ **Restaurar original**: descarta los cambios y vuelve a la imagen tal cual se cargó.
- 💾 **Guardar resultado** en formato PNG.
- 📊 **Histogramas** de intensidad (0–255) por canal, tanto de la imagen de entrada como del resultado, graficados con Matplotlib.

## Requisitos

- Python 3.8 o superior
- [NumPy](https://numpy.org/)
- [Pillow](https://python-pillow.org/)
- [Matplotlib](https://matplotlib.org/)
- Tkinter (incluido con la instalación estándar de Python en la mayoría de los sistemas; en Linux puede requerir instalar el paquete `python3-tk` por separado)

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/<tu-usuario>/<tu-repositorio>.git
cd <tu-repositorio>

# (Opcional pero recomendado) crear un entorno virtual
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt
```

Si en Linux `tkinter` no está disponible, instalarlo con:

```bash
sudo apt install python3-tk
```

## Uso

```bash
python TP0.py
```

1. Hacé clic en **Cargar Imagen** y seleccioná un archivo desde el disco.
2. Elegí una operación del panel izquierdo (**Escala de Grises**, **Canal Rojo**, **Canal Verde** o **Canal Azul**). El resultado aparece en el panel derecho.
3. Usá **Ver Hist. Entrada** o **Ver Hist. Resultado** para abrir el histograma de intensidades correspondiente.
4. Si querés seguir aplicando operaciones sobre el resultado, usá **Pasar Resultado a Entrada**.
5. Usá **Restaurar Original** para volver a la imagen tal cual se cargó.
6. Usá **Guardar PNG** para exportar la imagen resultado a disco.

## Estructura del proyecto

```
.
├── TP0.py            # Aplicación completa (interfaz + lógica de PDI)
├── requirements.txt    # Dependencias del proyecto
└── README.md            # Este archivo
```

Toda la aplicación está contenida en `TP0.py`, en la clase `PDIApp`, organizada en tres bloques:

| Bloque | Responsabilidad |
|---|---|
| Interfaz (`_crear_interfaz`, `actualizar_vistas`, `array_to_image_tk`) | Construcción de widgets de Tkinter y despliegue de imágenes |
| Procesamiento (`convertir_grises`, `aislar_canal`) | Transformaciones sobre las matrices NumPy de la imagen |
| Flujo de trabajo (`cargar_imagen`, `resultado_a_entrada`, `restaurar_original`, `guardar_resultado`) | Ciclo de vida de la imagen entre disco, entrada y resultado |
| Histogramas (`mostrar_histograma`) | Cálculo con `np.histogram` y graficado con Matplotlib |

## Cómo funciona

La imagen se representa siempre como un array de NumPy `uint8` (valores 0–255):

- **`img_original`**: la imagen tal cual se cargó del disco. No se modifica salvo al cargar una imagen nueva.
- **`img_entrada`**: la imagen sobre la que se aplica la próxima operación (panel izquierdo).
- **`img_resultado`**: el resultado de la última operación aplicada (panel derecho). Puede ser una matriz de 3 canales (RGB) o de 1 canal (escala de grises).

Flujo típico:

```
Cargar Imagen  →  img_original == img_entrada
       ↓
Aplicar operación (usa img_entrada)  →  guarda en img_resultado
       ↓
Pasar Resultado a Entrada  →  img_entrada = img_resultado
       ↓
(se puede volver a aplicar otra operación, encadenando procesos)
```

El histograma se calcula con `np.histogram(canal, bins=256, range=(0, 256))` por cada canal, y se grafica con `matplotlib.pyplot` en una ventana aparte (`plt.figure` + `plt.show`), sin bloquear la ventana principal de Tkinter.

## Cómo agregar nuevas operaciones

1. Agregar un método nuevo a la clase `PDIApp`, siguiendo el mismo patrón que `convertir_grises` o `aislar_canal`: leer de `self.img_entrada`, escribir en `self.img_resultado`, y llamar a `self.actualizar_vistas()` al final.
2. Agregar un botón en `_crear_interfaz()`, dentro de `ops_frame`, que llame a ese método.

Ejemplo esquemático:

```python
def ajustar_brillo(self, factor: float):
    if self.img_entrada is None:
        return
    resultado = np.clip(self.img_entrada.astype(np.float32) * factor, 0, 255)
    self.img_resultado = resultado.astype(np.uint8)
    self.actualizar_vistas()
```

## Limitaciones conocidas

- No hay historial de pasos intermedios: solo se puede volver a la imagen original, no deshacer un paso a la vez.
- Las imágenes se redimensionan a un máximo de 400x400 px solo para mostrarse en pantalla; el procesamiento y el guardado siempre usan la resolución completa.
- El histograma se abre en una ventana externa de Matplotlib (no está embebido en la ventana principal de Tkinter).

## Licencia

Este proyecto se distribuye bajo licencia MIT. Ver [LICENSE](LICENSE) para más detalles.
