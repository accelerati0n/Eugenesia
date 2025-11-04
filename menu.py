import pygame
from settings import BACKGROUND_DIR, WHITE, WIDTH, HEIGHT, LEVEL1_BG
from image_loader import ImageLoader
import os
import math

class Menu:
    def __init__(self, screen):
        self.screen = screen
        
        # Cargar fondo del menú usando LEVEL1_BG (rooftop.png)
        bg_path = LEVEL1_BG  # ✅ Usa la constante de settings
        if os.path.exists(bg_path):
            # Cargar con suavizado y escalar a pantalla completa
            bg_img = ImageLoader.load_smooth(bg_path)
            self.background, self.bg_rect = ImageLoader.scale_to_fit(
                bg_img, 
                screen.get_size(), 
                keep_aspect=True,
                center=True
            )
            print(f"✓ Fondo de menú cargado: {bg_path}")
        else:
            print(f"⚠️ No se encontró {bg_path}, usando fondo negro")
            self.background = pygame.Surface(screen.get_size())
            self.background.fill((0, 0, 0))
            self.bg_rect = self.background.get_rect()
        
        # Fuentes
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 36)
        
        # Textos
        self.title = self.title_font.render("EUGENESIA", True, (255, 100, 100))
        self.title_rect = self.title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        
        self.prompt = self.font.render("Presiona ENTER para comenzar", True, WHITE)
        self.prompt_rect = self.prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Efecto de parpadeo
        self.timer = 0
        self.alpha = 255

    def update(self, dt):
        """Actualiza el efecto de parpadeo del texto"""
        self.timer += dt * 4
        self.alpha = 128 + int(127 * abs(math.sin(self.timer)))

    def draw(self):
        """Dibuja el menú"""
        # Fondo negro completo
        self.screen.fill((0, 0, 0))
        
        # Dibujar fondo centrado
        self.screen.blit(self.background, self.bg_rect)
        
        # Título
        self.screen.blit(self.title, self.title_rect)
        
        # Texto parpadeante
        prompt_surface = self.prompt.copy()
        prompt_surface.set_alpha(self.alpha)
        self.screen.blit(prompt_surface, self.prompt_rect)

    def handle_event(self, event):
        """Maneja eventos del menú"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "start_game"
        return None
