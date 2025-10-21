"""
background.py
Clase Background para el fondo estático del juego
Hereda de GameObject
"""

import pygame
from base_classes import GameObject


class Background(GameObject):
    """
    Clase para el fondo estático del juego.
    Hereda de GameObject y maneja la imagen de fondo.
    """
    
    def __init__(self, image_path):
        """
        Constructor del fondo.
        
        Args:
            image_path (str): Ruta completa a la imagen de fondo
        """
        super().__init__(0, 0)
        self.image = None
        self.load_background(image_path)
    
    def load_background(self, path):
        """
        Carga la imagen de fondo desde un archivo.
        
        Args:
            path (str): Ruta al archivo de imagen
        """
        try:
            self.image = pygame.image.load(path).convert()
            print(f"✓ Fondo cargado: {self.image.get_size()}")
        except pygame.error as e:
            print(f"✗ Error cargando fondo {path}: {e}")
            self.image = None
    
    def update(self):
        """
        El fondo no necesita actualización.
        Implementa el método abstracto de GameObject.
        """
        pass
    
    def draw(self, screen):
        """
        Dibuja el fondo en la pantalla.
        Sobrescribe el método de GameObject (polimorfismo).
        
        Args:
            screen (pygame.Surface): Superficie donde dibujar
        """
        if self.image:
            screen.blit(self.image, (0, 0))
