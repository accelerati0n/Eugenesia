import pygame
from sounds import SoundManager
from level_city import CityLevel
from waiting_room_level import WaitingRoomLevel
from level_office import OfficeLevel

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.sound = SoundManager()
        self.level = CityLevel(screen)
        self.current_scene = "city"
        print("✓ Game inicializado")

    def play_music(self):
        self.sound.play_music("theme.mp3")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self, dt):
        """Actualiza la lógica del nivel actual"""
        next_scene = self.level.update(dt)
        
        if next_scene == "waiting_room":
            self.level = WaitingRoomLevel(self.screen)
            self.current_scene = "waiting_room"
            print("→ Cambio a nivel: WAITING ROOM")
        
        elif next_scene == "office":
            self.level = OfficeLevel(self.screen)
            self.current_scene = "office"
            print("→ Cambio a nivel: OFFICE")
        
        elif next_scene == "city":
            self.level = CityLevel(self.screen)
            self.current_scene = "city"
            print("→ Cambio a nivel: CITY")
        
        elif next_scene == "victory":
            print("🎉 VICTORIA - Hohen derrotado!")
        
        elif next_scene == "defeat":
            print("☠️ DERROTA - Volviendo a la ciudad...")
            self.level = CityLevel(self.screen)
            self.current_scene = "city"

    def draw(self):
        """Dibuja el nivel actual"""
        self.level.draw()
