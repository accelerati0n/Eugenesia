import pygame
import os
from settings import WHITE, BLACK, WIDTH, HEIGHT, LEVEL2_BG
from player import Player
from dialog_box import DialogSequence

class WaitingRoomLevel:
    """Nivel Waiting Room - Solo diálogos, luego presiona E para ir a Office"""
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        
        # Cargar fondo del waiting room
        bg_path = LEVEL2_BG
        if os.path.exists(bg_path):
            try:
                bg_img = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(bg_img, (self.screen_width, self.screen_height))
                print(f"✓ Fondo Waiting Room cargado: {bg_path}")
            except Exception as e:
                print(f"❌ Error cargando fondo: {e}")
                self.background = pygame.Surface((self.screen_width, self.screen_height))
                self.background.fill((40, 40, 50))
        else:
            print(f"⚠️ No se encontró {bg_path}")
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((40, 40, 50))
        
        # Crear jugador (solo para la escena)
        start_pos = (self.screen_width // 2, 500)
        self.player = Player(start_pos)
        self.all_sprites = pygame.sprite.Group(self.player)
        
        # Sistema de diálogos
        self.dialogs = [
            {
                'title': '🏢 BIENVENIDO A EUGENESIA',
                'text': '¡Bienvenido a la sala de espera de Eugenesia! Aquí comienza tu viaje hacia la perfección.'
            },
            {
                'title': '📈 TU MISIÓN',
                'text': 'Para alcanzar tu máximo perfeccionamiento en habilidades, debes subir y enfrentarte a los desafíos.'
            },
            {
                'title': '⚔️ BATALLAS',
                'text': 'En los niveles superiores te espera una horda de enemigos cada vez más fuertes. ¡Prepárate para pelear!'
            },
            {
                'title': '💪 GANA PODER',
                'text': 'Con cada enemigo derrotado, aumentarás tu poder y habilidades. ¡Demuestra de qué estás hecho!'
            },
            {
                'title': '🚀 ¡VAMOS!',
                'text': 'Los diálogos han terminado. Presiona E cuando estés listo para enfrentarte a Hohen el Oficinista.'
            }
        ]
        
        self.dialog_sequence = DialogSequence(self.screen, self.dialogs)
        self.show_dialog = True
        
        print("✓ Nivel Waiting Room cargado - Solo diálogos")

    def update(self, dt):
        """Actualiza la lógica del nivel"""
        if self.show_dialog:
            self.dialog_sequence.update(dt)
            self.dialog_sequence.handle_input()
            
            if self.dialog_sequence.is_finished():
                self.show_dialog = False
                print("▶ Diálogos completados - Presiona E para continuar")
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                print("→ ¡Yendo al Office para batalla con Hohen!")
                return "office"
        
        return None

    def draw(self):
        """Dibuja el nivel"""
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        
        if self.show_dialog:
            self.dialog_sequence.draw()
        else:
            font = pygame.font.Font(None, 28)
            text = font.render("Presiona E para continuar", True, (255, 255, 100))
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 200))
            
            bg_rect = text_rect.inflate(40, 20)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 180))
            self.screen.blit(bg_surface, bg_rect)
            
            self.screen.blit(text, text_rect)
