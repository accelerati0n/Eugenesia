import pygame
import os
import re
from settings import PLAYER_SIZE_MULTIPLIER

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        
        # Propiedades básicas
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        
        # HP
        self.hp = 100
        self.hp_max = 100
        
        # Sprites
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.15
        self.frame_timer = 0
        self.sprite_mode = "walk"
        self.damage_timer = 0
        
        # Cargar sprites de caminata
        self.load_walk_sprites()
        
        # Sprite actual
        self.image = self.frames[0] if self.frames else pygame.Surface((40, 60))
        self.rect = self.image.get_rect(center=pos)
        
        print(f"✓ Otto creado en posición {pos}")

    def load_walk_sprites(self):
        """Carga sprites de caminata - IGUAL QUE HOHEN"""
        sprite_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets", "sprites", "otto"
        )
        
        self.frames = []
        if os.path.exists(sprite_dir):
            try:
                # Buscar archivos frame_*.png O numerados como Hohen
                frame_files = [f for f in sorted(os.listdir(sprite_dir), key=lambda x: self._sort_key(x))
                              if (f.startswith("frame_") or (f[0].isdigit())) and f.endswith(".png")]
                
                print(f"📂 Encontrados {len(frame_files)} archivos en {sprite_dir}")
                
                for filename in frame_files:
                    frame_path = os.path.join(sprite_dir, filename)
                    try:
                        frame_img = pygame.image.load(frame_path).convert_alpha()
                        
                        # Escalar - MISMO SISTEMA QUE HOHEN
                        original_height = frame_img.get_height()
                        target_height = int(original_height * PLAYER_SIZE_MULTIPLIER)
                        scale_factor = target_height / original_height if original_height > 0 else 1
                        new_width = int(frame_img.get_width() * scale_factor)
                        
                        frame_img = pygame.transform.scale(frame_img, (new_width, target_height))
                        self.frames.append(frame_img)
                        print(f"  ✓ Sprite cargado: {filename}")
                    except Exception as e:
                        print(f"  ❌ Error cargando {filename}: {e}")
                
                if not self.frames:
                    print("⚠️ No se cargaron sprites, usando placeholder")
                    self.frames = [pygame.Surface((40, 60))]
                else:
                    print(f"✓ {len(self.frames)} sprites de caminata cargados")
            except Exception as e:
                print(f"❌ Error: {e}")
                self.frames = [pygame.Surface((40, 60))]
        else:
            print(f"❌ Carpeta no encontrada: {sprite_dir}")
            self.frames = [pygame.Surface((40, 60))]

    def load_fight_sprites(self):
        """Carga sprites de pelea - IGUAL QUE HOHEN"""
        sprite_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets", "sprites", "otto_fight"
        )
        
        fight_frames = []
        if os.path.exists(sprite_dir):
            try:
                # Buscar todos los archivos PNG
                fight_files = [f for f in sorted(os.listdir(sprite_dir), key=lambda x: self._sort_key(x))
                              if f.endswith(".png")]
                
                print(f"📂 Encontrados {len(fight_files)} sprites de pelea")
                
                for filename in fight_files:
                    # Saltar golpeado.png y standby.png (solo fight*)
                    if filename.lower() in ["golpeado.png", "standby.png"]:
                        continue
                    
                    frame_path = os.path.join(sprite_dir, filename)
                    try:
                        frame_img = pygame.image.load(frame_path).convert_alpha()
                        
                        # Escalar - MISMO SISTEMA QUE HOHEN
                        original_height = frame_img.get_height()
                        target_height = int(original_height * PLAYER_SIZE_MULTIPLIER)
                        scale_factor = target_height / original_height if original_height > 0 else 1
                        new_width = int(frame_img.get_width() * scale_factor)
                        
                        frame_img = pygame.transform.scale(frame_img, (new_width, target_height))
                        fight_frames.append(frame_img)
                        print(f"  ✓ Sprite de pelea: {filename}")
                    except Exception as e:
                        print(f"  ❌ Error: {e}")
                
                if fight_frames:
                    self.frames = fight_frames
                    print(f"✓ {len(self.frames)} sprites de pelea cargados")
            except Exception as e:
                print(f"❌ Error en load_fight_sprites: {e}")
        else:
            print(f"❌ Carpeta no encontrada: {sprite_dir}")

    def load_damage_sprite(self):
        """Carga sprite de daño"""
        sprite_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets", "sprites", "otto_fight"
        )
        
        damage_path = os.path.join(sprite_dir, "golpeado.png")
        if os.path.exists(damage_path):
            try:
                damage_img = pygame.image.load(damage_path).convert_alpha()
                
                original_height = damage_img.get_height()
                target_height = int(original_height * PLAYER_SIZE_MULTIPLIER)
                scale_factor = target_height / original_height if original_height > 0 else 1
                new_width = int(damage_img.get_width() * scale_factor)
                
                damage_img = pygame.transform.scale(damage_img, (new_width, target_height))
                self.frames = [damage_img]
                print("✓ Sprite de daño cargado")
            except Exception as e:
                print(f"❌ Error: {e}")

    def _sort_key(self, filename):
        """Ordena archivos numéricos correctamente"""
        match = re.match(r'(\d+)', filename)
        if match:
            return int(match.group(1))
        return float('inf')

    def set_damage_mode(self, duration=0.5):
        """Activa modo de daño"""
        self.load_damage_sprite()
        self.sprite_mode = "damage"
        self.damage_timer = duration
        print("💔 Otto golpeado")

    def update(self, dt):
        """Actualiza el jugador"""
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        
        if keys[pygame.K_a]:
            self.velocity.x = -150
        elif keys[pygame.K_d]:
            self.velocity.x = 150
        
        self.pos.x += self.velocity.x * dt
        self.pos.y += self.velocity.y * dt
        
        self.velocity.y += 1000 * dt
        
        # Actualizar tiempo de daño
        if self.sprite_mode == "damage":
            self.damage_timer -= dt
            if self.damage_timer <= 0:
                self.sprite_mode = "walk"
                self.load_walk_sprites()
                self.current_frame = 0
        
        # Actualizar animación
        self.frame_timer += dt
        if self.frame_timer >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.frame_timer = 0
        
        # self.rect.center = self.pos.x

    def draw(self, surface):
        surface.blit(self.image, self.rect)
