"""
character.py
Clase Character para personajes con movimiento y animación
Implementa herencia de Entity y define comportamiento base para personajes
"""

import pygame
import os
from abc import abstractmethod
from base_classes import Entity
from constants import ANIMATION_SPEED


class Character(Entity):
    """
    Clase base para personajes con movimiento y animación.
    Hereda de Entity y añade funcionalidad de animación y movimiento.
    """

    def __init__(self, x, y, frames_folder):
        """
        Constructor para personajes animados.

        Args:
            x (float): Posición inicial en el eje X
            y (float): Posición inicial en el eje Y
            frames_folder (str): Ruta a la carpeta con los frames de animación
        """
        super().__init__(x, y)
        self.frames_folder = frames_folder
        self.frames = []
        self.current_frame = 0
        self.animation_counter = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_moving = False
        self.direction = "idle"  # "left", "right", "idle"

    @abstractmethod
    def load_animations(self):
        """
        Carga las animaciones del personaje.
        Método abstracto que debe ser implementado por las clases hijas.
        """
        pass

    def animate(self):
        """
        Maneja la animación del personaje según su estado de movimiento.
        Cambia entre frames cuando el personaje se mueve.
        """
        if self.is_moving and len(self.frames) > 0:
            self.animation_counter += 1
            if self.animation_counter >= ANIMATION_SPEED:
                self.animation_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.sprite = self.frames[self.current_frame]
        else:
            # Frame idle (frontal) cuando no se mueve
            if len(self.frames) >= 6:
                self.sprite = self.frames[5]  # Frame 6 es la pose frontal
                self.current_frame = 5

    def update(self):
        """
        Actualiza la animación y posición del personaje.
        Sobrescribe el método de Entity (polimorfismo).
        """
        self.animate()
        if self.rect:
            self.rect.center = (self.x, self.y)
