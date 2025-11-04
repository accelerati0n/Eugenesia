import os

# ========================================
# DIRECTORIOS Y RUTAS
# ========================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")
SFX_DIR = os.path.join(ASSETS_DIR, "sfx")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
BACKGROUNDS_DIR = os.path.join(ASSETS_DIR, "backgrounds")

# Sprites específicos
PLAYER_OTTO_DIR = os.path.join(SPRITES_DIR, "otto")
BACKGROUND_DIR = BACKGROUNDS_DIR

# Fondos específicos
LEVEL1_BG = os.path.join(BACKGROUNDS_DIR, "rooftop.png")
LEVEL2_BG = os.path.join(BACKGROUNDS_DIR, "waiting_room.png")
LEVEL3_BG = os.path.join(BACKGROUNDS_DIR, "office.png")

# ========================================
# CONFIGURACIÓN DE PANTALLA
# ========================================

WIDTH = 1280
HEIGHT = 720
FPS = 60

# Resolución interna del juego (para pixel art)
GAME_WIDTH = 320
GAME_HEIGHT = 180

# ========================================
# COLORES RGB
# ========================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Colores personalizados
DARK_BLUE = (0, 0, 100)
DARK_GREEN = (0, 100, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# ========================================
# CONFIGURACIÓN DEL JUGADOR
# ========================================

PLAYER_SPEED = 150
PLAYER_JUMP_FORCE = -350
PLAYER_GRAVITY = 1000
PLAYER_SIZE_MULTIPLIER = 0.5

# ========================================
# CONFIGURACIÓN DE NIVELES
# ========================================

SIDEWALK_Y_MIN = 600
SIDEWALK_Y_MAX = 600

# ========================================
# CONFIGURACIÓN DE AUDIO
# ========================================

MASTER_VOLUME = 0.5
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7

# ========================================
# CONFIGURACIÓN DE ENEMIGOS
# ========================================

MAX_ENEMIES = 5
ENEMY_SPAWN_INTERVAL = 5
ENEMY_BASE_SPEED = 2

# ========================================
# CONFIGURACIÓN DE EFECTOS VISUALES
# ========================================

USE_SMOOTHSCALE = True
ENABLE_VSYNC = True
SCREEN_RESIZABLE = True

# ========================================
# INFORMACIÓN DEL JUEGO
# ========================================

GAME_TITLE = "Eugenesia"
GAME_VERSION = "1.0"
AUTHOR = "Tu Nombre"
