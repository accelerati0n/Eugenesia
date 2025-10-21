"""
game.py
Clase Game que maneja el loop principal del juego
Coordina todos los objetos y sistemas del juego
"""

import pygame
import sys
import os
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK,
    BASE_PATH, BACKGROUND_IMAGE, FRAMES_FOLDER,
    SIDEWALK_TOP, SIDEWALK_BOTTOM
)
from background import Background
from player import Player


class Game:
    """
    Clase principal que maneja el loop del juego.
    Coordina la inicialización, actualización y renderizado.
    """
    
    def __init__(self):
        """
        Constructor del juego.
        Inicializa Pygame, crea la ventana y los objetos del juego.
        """
        # Inicializar Pygame
        pygame.init()
        
        # Crear ventana
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Eugenesia - Start Page")
        
        # Clock para controlar FPS
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Configurar rutas de archivos
        self.background_path = os.path.join(BASE_PATH, BACKGROUND_IMAGE)
        self.frames_path = os.path.join(BASE_PATH, FRAMES_FOLDER)
        
        # Crear objetos del juego
        print("\n=== Inicializando Eugenesia ===")
        self.background = Background(self.background_path)
        self.player = Player(
            SCREEN_WIDTH // 2, 
            SIDEWALK_TOP + 50, 
            self.frames_path
        )
        
        # Lista de todos los objetos del juego (polimorfismo)
        self.game_objects = [self.background, self.player]
        
        print("=== Inicialización completada ===\n")
    
    def handle_events(self):
        """
        Maneja los eventos de Pygame (cerrar ventana, teclas, etc.)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """
        Actualiza todos los objetos del juego.
        Demuestra polimorfismo: cada objeto tiene su propio update().
        """
        # Obtener estado de las teclas
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        # Actualizar todos los objetos (polimorfismo en acción)
        for obj in self.game_objects:
            obj.update()
    
    def draw(self):
        """
        Dibuja todos los objetos en la pantalla.
        Demuestra polimorfismo: cada objeto tiene su propio draw().
        """
        # Limpiar pantalla
        self.screen.fill(BLACK)
        
        # Dibujar todos los objetos (polimorfismo en acción)
        for obj in self.game_objects:
            obj.draw(self.screen)
        
        # Opcional: Dibujar líneas de debug para ver los límites del andén
        # pygame.draw.line(self.screen, (255, 0, 0), 
        #                  (0, SIDEWALK_TOP), (SCREEN_WIDTH, SIDEWALK_TOP), 2)
        # pygame.draw.line(self.screen, (255, 0, 0), 
        #                  (0, SIDEWALK_BOTTOM), (SCREEN_WIDTH, SIDEWALK_BOTTOM), 2)
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def run(self):
        """
        Loop principal del juego.
        Ejecuta el ciclo de eventos -> actualizar -> dibujar.
        """
        print("🎮 Juego iniciado. Presiona ESC para salir.\n")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Cerrar Pygame al terminar
        pygame.quit()
        sys.exit()
