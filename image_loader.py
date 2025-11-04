import pygame
import os

class ImageLoader:
    """Gestor centralizado para cargar imágenes con calidad mejorada"""
    
    @staticmethod
    def load_smooth(path, scale=None, target_size=None):
        """
        Carga imagen con suavizado de alta calidad
        
        Args:
            path: Ruta de la imagen
            scale: Factor de escala (ej: 0.5 para 50%, 2.0 para 200%)
            target_size: Tupla (ancho, alto) para tamaño específico
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Imagen no encontrada: {path}")
        
        img = pygame.image.load(path).convert_alpha()
        
        if target_size:
            img = pygame.transform.smoothscale(img, target_size)
        elif scale:
            w, h = img.get_size()
            new_size = (int(w * scale), int(h * scale))
            img = pygame.transform.smoothscale(img, new_size)
        
        return img
    
    @staticmethod
    def load_frames_smooth(directory, count, scale=None, target_height=None):
        """
        Carga múltiples frames con suavizado
        
        Args:
            directory: Carpeta con los frames
            count: Número de frames
            scale: Factor de escala
            target_height: Altura objetivo (mantiene proporción)
        """
        frames = []
        for i in range(1, count + 1):
            frame_path = os.path.join(directory, f"frame_{i:02}.png")
            if os.path.exists(frame_path):
                img = pygame.image.load(frame_path).convert_alpha()
                
                if target_height:
                    w, h = img.get_size()
                    aspect_ratio = w / h
                    new_w = int(target_height * aspect_ratio)
                    img = pygame.transform.smoothscale(img, (new_w, target_height))
                elif scale:
                    w, h = img.get_size()
                    new_size = (int(w * scale), int(h * scale))
                    img = pygame.transform.smoothscale(img, new_size)
                
                frames.append(img)
        
        if not frames:
            raise FileNotFoundError(f"No se encontraron frames en {directory}")
        
        return frames
    
    @staticmethod
    def scale_to_fit(image, target_size, keep_aspect=True, center=True):
        """
        Escala imagen para ajustarla a un tamaño objetivo
        
        Args:
            image: Surface de Pygame
            target_size: Tupla (ancho, alto) objetivo
            keep_aspect: Mantener proporción de aspecto
            center: Centrar la imagen
        
        Returns:
            Tupla (surface_escalada, rect_posicion)
        """
        if keep_aspect:
            img_w, img_h = image.get_size()
            target_w, target_h = target_size
            
            # Calcular escala manteniendo proporción
            scale = min(target_w / img_w, target_h / img_h)
            new_size = (int(img_w * scale), int(img_h * scale))
            
            scaled_img = pygame.transform.smoothscale(image, new_size)
            
            if center:
                img_rect = scaled_img.get_rect(center=(target_w // 2, target_h // 2))
            else:
                img_rect = scaled_img.get_rect(topleft=(0, 0))
            
            return scaled_img, img_rect
        else:
            scaled_img = pygame.transform.smoothscale(image, target_size)
            return scaled_img, scaled_img.get_rect(topleft=(0, 0))
