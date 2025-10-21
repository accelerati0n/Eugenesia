"""
player.py
Clase Player para el jugador controlable
Implementa herencia de Character y añade control de usuario y restricciones
"""

import pygame
import os
from character import Character
from constants import (
    CHARACTER_SCALE, MOVEMENT_SPEED,
    SIDEWALK_TOP, SIDEWALK_BOTTOM, 
    SIDEWALK_LEFT, SIDEWALK_RIGHT
)


class Player(Character):
    """
    Clase del jugador principal con controles de teclado y restricciones de movimiento.
    Hereda de Character y añade funcionalidad específica del jugador.
    Demuestra polimorfismo al sobrescribir métodos de la clase padre.
    """

    def __init__(self, x, y, frames_folder):
        """
        Constructor del jugador.

        Args:
            x (float): Posición inicial en el eje X
            y (float): Posición inicial en el eje Y
            frames_folder (str): Ruta a la carpeta con los frames de animación
        """
        super().__init__(x, y, frames_folder)
        self.load_animations()
        self.boundaries = {
            "top": SIDEWALK_TOP,
            "bottom": SIDEWALK_BOTTOM,
            "left": SIDEWALK_LEFT,
            "right": SIDEWALK_RIGHT
        }

    def load_animations(self):
        """
        Carga todos los frames de animación del jugador desde la carpeta.
        Redimensiona cada frame según CHARACTER_SCALE.
        Implementa el método abstracto de Character.
        """
        try:
            # Cargar los 16 frames de animación
            for i in range(1, 17):
                frame_path = os.path.join(self.frames_folder, f"frame_{i:02d}.png")

                # Cargar imagen con transparencia
                frame = pygame.image.load(frame_path).convert_alpha()

                # Redimensionar el frame según la escala configurada
                original_size = frame.get_size()
                new_size = (
                    int(original_size[0] * CHARACTER_SCALE), 
                    int(original_size[1] * CHARACTER_SCALE)
                )
                frame = pygame.transform.scale(frame, new_size)

                self.frames.append(frame)

            # Establecer sprite inicial (pose frontal)
            if len(self.frames) > 5:
                self.sprite = self.frames[5]  # Frame 6 - pose frontal
                self.rect = self.sprite.get_rect(center=(self.x, self.y))

            print(f"✓ {len(self.frames)} frames de animación cargados")

        except Exception as e:
            print(f"✗ Error cargando animaciones: {e}")

    def handle_input(self, keys):
        """
        Maneja la entrada del teclado para controlar al jugador.
        Método específico de Player (polimorfismo).

        Args:
            keys (pygame.key.ScancodeWrapper): Estado actual de las teclas
        """
        # Resetear velocidades
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_moving = False

        # Movimiento horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -MOVEMENT_SPEED
            self.direction = "left"
            self.is_moving = True

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = MOVEMENT_SPEED
            self.direction = "right"
            self.is_moving = True

        # Movimiento vertical (solo en el andén)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = -MOVEMENT_SPEED
            self.is_moving = True

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = MOVEMENT_SPEED
            self.is_moving = True

    def apply_boundaries(self):
        """
        Aplica las restricciones de movimiento para mantener al jugador en el andén.
        Evita que el jugador salga de los límites establecidos.
        """
        # Restricción horizontal
        if self.x < self.boundaries["left"]:
            self.x = self.boundaries["left"]
        elif self.x > self.boundaries["right"]:
            self.x = self.boundaries["right"]

        # Restricción vertical (andén)
        if self.y < self.boundaries["top"]:
            self.y = self.boundaries["top"]
        elif self.y > self.boundaries["bottom"]:
            self.y = self.boundaries["bottom"]

    def update(self):
        """
        Actualiza la posición y animación del jugador cada frame.
        Sobrescribe el método de Character (polimorfismo).
        """
        # Aplicar velocidad a la posición
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Aplicar restricciones de movimiento
        self.apply_boundaries()

        # Actualizar animación (método heredado de Character)
        self.animate()

        # Actualizar rect para colisiones y dibujo
        if self.rect:
            self.rect.center = (self.x, self.y)
