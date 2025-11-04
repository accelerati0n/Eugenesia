import pygame
import sys
from settings import WIDTH, HEIGHT, FPS
from menu import Menu
from game import Game

class GameEngine:
    """Motor principal del juego Eugenesia"""
    
    def __init__(self):
        """Inicializa el motor del juego"""
        pygame.init()
        
        # Configurar pantalla
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Eugenesia - 8-bit Adventure")
        pygame.display.set_icon(self.create_icon())
        
        # Clock para controlar FPS
        self.clock = pygame.time.Clock()
        self.dt = 0  # Delta time
        self.fps = FPS
        
        # Estados del juego
        self.current_state = "menu"  # menu, game, paused
        self.menu = Menu(self.screen)
        self.game = None
        
        print("╔════════════════════════════════════════╗")
        print("║         EUGENESIA - 8-bit Game         ║")
        print("║         Version 1.0 - Mejorada         ║")
        print("╚════════════════════════════════════════╝")
        print(f"\n✓ Resolución: {WIDTH}x{HEIGHT}")
        print(f"✓ FPS Target: {FPS}")
        # print(f"✓ Pygame versión: {pygame.__version__}\n")

    def create_icon(self):
        """Crea un icono simple para la ventana"""
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        # Dibuja un pequeño cuadrado de color
        pygame.draw.rect(icon, (255, 100, 100), (0, 0, 32, 32))
        pygame.draw.rect(icon, (255, 255, 255), (0, 0, 32, 32), 2)
        return icon

    def handle_events(self):
        """Maneja todos los eventos del juego"""
        for event in pygame.event.get():
            # Cerrar ventana
            if event.type == pygame.QUIT:
                return False
            
            # Tecla ESC para salir
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                # En menú: ENTER para empezar
                if self.current_state == "menu":
                    if event.key == pygame.K_RETURN:
                        self.start_game()
                
                # En pausa: SPACE para reanudar
                elif self.current_state == "paused":
                    if event.key == pygame.K_SPACE:
                        self.current_state = "game"
                
                # En juego: P para pausar
                elif self.current_state == "game":
                    if event.key == pygame.K_p:
                        self.current_state = "paused"
            
            # Redimensionar ventana
            if event.type == pygame.VIDEORESIZE:
                if event.size[0] > 320 and event.size[1] > 180:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        
        return True

    def start_game(self):
        """Inicia el juego"""
        self.game = Game(self.screen)
        self.current_state = "game"
        print("▶ JUEGO INICIADO\n")

    def update(self):
        """Actualiza la lógica del juego"""
        if self.current_state == "menu":
            self.menu.update(self.dt)
        
        elif self.current_state == "game" and self.game:
            self.game.update(self.dt)

    def draw(self):
        """Dibuja el juego"""
        self.screen.fill((0, 0, 0))
        
        if self.current_state == "menu":
            self.menu.draw()
        
        elif self.current_state == "game" and self.game:
            self.game.draw()
        
        elif self.current_state == "paused" and self.game:
            # Dibujar el juego pausado con overlay
            self.game.draw()
            
            # Overlay semi-transparente
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            
            # Texto de pausa
            font = pygame.font.Font(None, 72)
            pause_text = font.render("PAUSED", True, (255, 255, 255))
            text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            self.screen.blit(pause_text, text_rect)
            
            # Instrucciones
            small_font = pygame.font.Font(None, 32)
            continue_text = small_font.render("Presiona SPACE para continuar", True, (200, 200, 200))
            continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(continue_text, continue_rect)
        
        # Mostrar FPS en la esquina
        self.draw_fps()
        
        # Actualizar pantalla
        pygame.display.flip()

    def draw_fps(self):
        """Dibuja el contador de FPS en la pantalla"""
        font = pygame.font.Font(None, 24)
        fps_text = font.render(f"FPS: {int(self.clock.get_fps())}", True, (100, 255, 100))
        self.screen.blit(fps_text, (10, 10))

    def run(self):
        """Loop principal del juego"""
        running = True
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("CONTROLES:")
        print("  A/D o Flechas: Mover")
        print("  SPACE: Saltar")
        print("  E: Interactuar")
        print("  P: Pausar")
        print("  ESC: Salir")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        while running:
            # Eventos
            running = self.handle_events()
            
            # Actualizar (con delta time)
            self.dt = self.clock.tick(self.fps) / 1000.0  # Convertir a segundos
            self.update()
            
            # Dibujar
            self.draw()
        
        self.quit()

    def quit(self):
        """Cierra el juego correctamente"""
        print("\n" + "━" * 40)
        print("Cerrando Eugenesia...")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    """Punto de entrada del programa"""
    engine = GameEngine()
    engine.run()
