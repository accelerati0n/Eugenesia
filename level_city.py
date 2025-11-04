import pygame
import os
from settings import BACKGROUND_DIR, SIDEWALK_Y_MIN, SIDEWALK_Y_MAX, WIDTH, HEIGHT, LEVEL1_BG
from player import Player

class CityLevel:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        
        # Cargar fondo de la ciudad
        bg_path = LEVEL1_BG
        if os.path.exists(bg_path):
            try:
                bg_img = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(bg_img, (self.screen_width, self.screen_height))
                print(f"✓ Fondo ciudad cargado: {bg_path}")
            except Exception as e:
                print(f"❌ Error cargando fondo: {e}")
                self.background = pygame.Surface((self.screen_width, self.screen_height))
                self.background.fill((50, 50, 80))
        else:
            print(f"⚠️ No se encontró {bg_path}")
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((50, 50, 80))
        
        # Crear jugador
        start_pos = (self.screen_width // 2, SIDEWALK_Y_MAX)
        self.player = Player(start_pos)
        self.all_sprites = pygame.sprite.Group(self.player)
        
        # Zona de puerta para entrar al edificio
        door_width = 100
        door_height = 80
        door_x = self.screen_width // 2 - door_width // 2
        door_y = SIDEWALK_Y_MAX - door_height
        self.door_rect = pygame.Rect(door_x, door_y, door_width, door_height)
        
        # Indicador de puerta
        self.show_door_prompt = False

    def update(self, dt):
        """Actualiza la lógica del nivel"""
        # Actualizar jugador
        self.player.update(dt)
        
        # Limitar movimiento del jugador a los bordes de la pantalla
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.rect.right > self.screen_width:
            self.player.rect.right = self.screen_width
        
        # Limitar movimiento vertical a la acera
        if self.player.rect.bottom < SIDEWALK_Y_MIN:
            self.player.rect.bottom = SIDEWALK_Y_MIN
        if self.player.rect.bottom > SIDEWALK_Y_MAX:
            self.player.rect.bottom = SIDEWALK_Y_MAX
        
        # Verificar si el jugador está cerca de la puerta
        if self.player.rect.colliderect(self.door_rect):
            self.show_door_prompt = True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e] or keys[pygame.K_UP]:
                return "waiting_room"
        else:
            self.show_door_prompt = False
        
        return None

    def draw(self):
        """Dibuja el nivel"""
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        
        # Indicador visual de la puerta
        if self.show_door_prompt:
            font = pygame.font.Font(None, 24)
            text = font.render("Presiona E para entrar", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.door_rect.centerx, self.door_rect.top - 20))
            
            bg_rect = text_rect.inflate(20, 10)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 180))
            self.screen.blit(bg_surface, bg_rect)
            self.screen.blit(text, text_rect)
