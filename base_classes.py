"""
base_classes.py
Clases base abstractas para todos los objetos del juego
Implementa herencia y polimorfismo
"""

import pygame
from abc import ABC, abstractmethod


class GameObject(ABC):
    """
    Clase base abstracta para todos los objetos del juego.
    Define la interfaz común que todos los objetos deben implementar.
    """

    def __init__(self, x, y):
        """
        Constructor base para objetos del juego.

        Args:
            x (float): Posición inicial en el eje X
            y (float): Posición inicial en el eje Y
        """
        self.x = x
        self.y = y

    @abstractmethod
    def update(self):
        """
        Actualiza el estado del objeto cada frame.
        Método abstracto que debe ser implementado por las clases hijas.
        """
        pass

    @abstractmethod
    def draw(self, screen):
        """
        Dibuja el objeto en la pantalla.
        Método abstracto que debe ser implementado por las clases hijas.

        Args:
            screen (pygame.Surface): Superficie donde dibujar el objeto
        """
        pass


class Entity(GameObject):
    """
    Clase base para entidades que tienen sprites y animaciones.
    Hereda de GameObject y añade funcionalidad de gráficos.
    """

    def __init__(self, x, y, sprite_path=None):
        """
        Constructor para entidades con sprites.

        Args:
            x (float): Posición inicial en el eje X
            y (float): Posición inicial en el eje Y
            sprite_path (str, optional): Ruta al archivo de imagen del sprite
        """
        super().__init__(x, y)
        self.sprite = None
        self.rect = None
        if sprite_path:
            self.load_sprite(sprite_path)

    def load_sprite(self, path):
        """
        Carga un sprite desde un archivo de imagen.

        Args:
            path (str): Ruta al archivo de imagen
        """
        try:
            self.sprite = pygame.image.load(path).convert_alpha()
            self.rect = self.sprite.get_rect(center=(self.x, self.y))
            print(f"Sprite cargado: {path}")
        except pygame.error as e:
            print(f"Error cargando sprite {path}: {e}")

    def update(self):
        """
        Actualiza la posición del rect con las coordenadas actuales.
        Implementación base del método abstracto.
        """
        if self.rect:
            self.rect.center = (self.x, self.y)

    def draw(self, screen):
        """
        Dibuja el sprite en la pantalla.
        Implementación base del método abstracto.

        Args:
            screen (pygame.Surface): Superficie donde dibujar
        """
        if self.sprite and self.rect:
            screen.blit(self.sprite, self.rect)
