import pygame
import os
from settings import MUSIC_DIR, SFX_DIR

class SoundManager:
    def __init__(self):
        """Inicializa el gestor de sonidos"""
        pygame.mixer.init()
        
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        
        self.current_music = None
        self.sounds = {}
        
        print("✓ Gestor de sonidos inicializado")

    def load_music(self, filename):
        """Carga música desde la carpeta music"""
        music_path = os.path.join(MUSIC_DIR, filename)
        
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                self.current_music = filename
                print(f"✓ Música cargada: {filename}")
                return True
            except pygame.error as e:
                print(f"❌ Error cargando música: {e}")
                return False
        else:
            print(f"⚠️ Archivo de música no encontrado: {music_path}")
            return False

    def load_sound(self, sound_id, filename):
        """Carga un efecto de sonido"""
        sound_path = os.path.join(SFX_DIR, filename)
        
        if os.path.exists(sound_path):
            try:
                self.sounds[sound_id] = pygame.mixer.Sound(sound_path)
                self.sounds[sound_id].set_volume(self.sfx_volume)
                print(f"✓ Sonido cargado: {sound_id}")
                return True
            except pygame.error as e:
                print(f"❌ Error cargando sonido {sound_id}: {e}")
                return False
        else:
            print(f"⚠️ Archivo de sonido no encontrado: {sound_path}")
            return False

    def play_music(self, filename, loops=-1):
        """Reproduce música en loop"""
        if self.load_music(filename):
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops)

    def play_sound(self, sound_id):
        """Reproduce un efecto de sonido"""
        if sound_id in self.sounds:
            self.sounds[sound_id].play()
        else:
            print(f"⚠️ Sonido no encontrado: {sound_id}")

    def stop_music(self):
        """Detiene la música"""
        pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        """Ajusta el volumen de la música (0.0 a 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        """Ajusta el volumen de efectos de sonido (0.0 a 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

    def pause_music(self):
        """Pausa la música"""
        pygame.mixer.music.pause()

    def unpause_music(self):
        """Reanuda la música"""
        pygame.mixer.music.unpause()
