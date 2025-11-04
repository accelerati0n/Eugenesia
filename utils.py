import pygame
import os
import math

def load_image(path, scale=None):
    """
    Carga una imagen con suavizado
    
    Args:
        path: Ruta de la imagen
        scale: Factor de escala opcional
    
    Returns:
        Surface de Pygame
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Imagen no encontrada: {path}")
    
    img = pygame.image.load(path).convert_alpha()
    
    if scale:
        w, h = img.get_size()
        new_size = (int(w * scale), int(h * scale))
        img = pygame.transform.smoothscale(img, new_size)
    
    return img


def draw_text(surface, text, font, color, pos, center=False, alpha=255):
    """
    Dibuja texto en la pantalla
    
    Args:
        surface: Surface de Pygame
        text: Texto a dibujar
        font: Fuente de Pygame
        color: Color en RGB
        pos: Tupla (x, y) de posición
        center: Si True, centra el texto
        alpha: Valor de transparencia (0-255)
    """
    text_surface = font.render(text, True, color)
    
    if alpha < 255:
        text_surface.set_alpha(alpha)
    
    if center:
        rect = text_surface.get_rect(center=pos)
    else:
        rect = text_surface.get_rect(topleft=pos)
    
    surface.blit(text_surface, rect)


def draw_rect_outline(surface, rect, color, width=1, rounded=False, radius=0):
    """
    Dibuja el contorno de un rectángulo
    
    Args:
        surface: Surface de Pygame
        rect: Rectángulo de Pygame
        color: Color en RGB
        width: Grosor de la línea
        rounded: Si True, usa esquinas redondeadas
        radius: Radio de las esquinas
    """
    if rounded:
        pygame.draw.rect(surface, color, rect, width, border_radius=radius)
    else:
        pygame.draw.rect(surface, color, rect, width)


def draw_health_bar(surface, pos, current, max_hp, width=100, height=10):
    """
    Dibuja una barra de vida
    
    Args:
        surface: Surface de Pygame
        pos: Tupla (x, y) de posición
        current: Vida actual
        max_hp: Vida máxima
        width: Ancho de la barra
        height: Alto de la barra
    """
    x, y = pos
    
    # Fondo rojo
    pygame.draw.rect(surface, (255, 0, 0), (x, y, width, height))
    
    # Barra de vida (verde)
    bar_width = (current / max_hp) * width
    pygame.draw.rect(surface, (0, 255, 0), (x, y, bar_width, height))
    
    # Borde blanco
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)


def distance(pos1, pos2):
    """
    Calcula la distancia euclidiana entre dos puntos
    
    Args:
        pos1: Tupla (x1, y1)
        pos2: Tupla (x2, y2)
    
    Returns:
        Distancia en píxeles
    """
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def clamp(value, min_value, max_value):
    """
    Limita un valor entre un mínimo y máximo
    
    Args:
        value: Valor a limitar
        min_value: Valor mínimo
        max_value: Valor máximo
    
    Returns:
        Valor limitado
    """
    return max(min_value, min(value, max_value))


def lerp(start, end, t):
    """
    Interpolación lineal entre dos valores
    
    Args:
        start: Valor inicial
        end: Valor final
        t: Factor entre 0 y 1
    
    Returns:
        Valor interpolado
    """
    return start + (end - start) * t


def draw_circle_outline(surface, center, radius, color, width=1):
    """
    Dibuja el contorno de un círculo
    
    Args:
        surface: Surface de Pygame
        center: Tupla (x, y) del centro
        radius: Radio del círculo
        color: Color en RGB
        width: Grosor de la línea
    """
    pygame.draw.circle(surface, color, center, radius, width)


def fade_surface(surface, alpha):
    """
    Aplica transparencia a una surface
    
    Args:
        surface: Surface de Pygame
        alpha: Valor de transparencia (0-255)
    
    Returns:
        Surface con transparencia aplicada
    """
    copy = surface.copy()
    copy.set_alpha(alpha)
    return copy
