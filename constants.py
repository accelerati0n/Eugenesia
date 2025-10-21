"""
constants.py
Constantes globales del juego Eugenesia
"""

# Configuración de pantalla
SCREEN_WIDTH = 1227
SCREEN_HEIGHT = 738
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Configuración del personaje
CHARACTER_SCALE = 0.3  # Escala del personaje (30% del tamaño original)
MOVEMENT_SPEED = 5

# Límites del andén (sidewalk boundaries)
SIDEWALK_TOP = 450      # Límite superior del andén
SIDEWALK_BOTTOM = 550   # Límite inferior del andén
SIDEWALK_LEFT = 0
SIDEWALK_RIGHT = SCREEN_WIDTH

# Configuración de animación
ANIMATION_SPEED = 8  # Frames de juego entre cambios de sprite

# Rutas de archivos
BASE_PATH = r"C:\Users\150325\Desktop\Eugenesia\Images"
BACKGROUND_IMAGE = "start_page.png"
FRAMES_FOLDER = "movementes"
