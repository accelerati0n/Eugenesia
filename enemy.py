import pygame
import os
import random
import re
from settings import PLAYER_SIZE_MULTIPLIER

class Enemy(pygame.sprite.Sprite):
    """Clase base para enemigos"""
    
    def __init__(self, pos, name="Enemigo", hp=100, speed=2, sprite_dir=None):
        super().__init__()
        self.name = name
        self.pos = pygame.Vector2(pos)
        self.speed = speed
        
        self.hp = hp
        self.hp_max = hp
        
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.1
        self.frame_timer = 0
        
        if sprite_dir and os.path.exists(sprite_dir):
            self.load_animations(sprite_dir)
            self.image = self.frames[0] if self.frames else pygame.Surface((80, 80))
        else:
            self.image = pygame.Surface((80, 80))
            self.image.fill((255, 0, 0))
            self.frames = [self.image]
        
        self.rect = self.image.get_rect(center=pos)
        
        self.attack_cooldown = 0
        self.attack_delay = 2
        self.is_attacking = False
        self.attack_range = 150
        
        print(f"✓ Enemigo creado: {name} ({hp} HP)")

    def load_animations(self, sprite_dir):
        """Carga animaciones - 70% del tamaño de Otto"""
        try:
            frames_list = []
            
            for filename in sorted(os.listdir(sprite_dir), key=lambda x: self._sort_key(x)):
                if (filename[0].isdigit() and filename.endswith(".png")) or \
                   (filename.startswith("frame_") and filename.endswith(".png")):
                    
                    frame_path = os.path.join(sprite_dir, filename)
                    try:
                        frame_img = pygame.image.load(frame_path).convert_alpha()
                        
                        # ✅ 70% del tamaño de Otto para equilibrio
                        original_height = frame_img.get_height()
                        target_height = int(original_height * PLAYER_SIZE_MULTIPLIER * 0.099)
                        scale_factor = target_height / original_height if original_height > 0 else 1
                        new_width = int(frame_img.get_width() * scale_factor)
                        
                        frame_img = pygame.transform.scale(frame_img, (new_width, target_height))
                        frames_list.append(frame_img)
                        print(f"  ✓ Cargado: {filename}")
                    except Exception as e:
                        print(f"  ❌ Error cargando {filename}: {e}")
            
            self.frames = frames_list if frames_list else [pygame.Surface((80, 80))]
            print(f"✓ Total: {len(self.frames)} frames cargados para {self.name}")
        except Exception as e:
            print(f"❌ Error cargando sprites de {self.name}: {e}")
            self.frames = [pygame.Surface((80, 80))]

    def _sort_key(self, filename):
        """Ordena archivos numéricos correctamente"""
        match = re.match(r'(\d+)', filename)
        if match:
            return int(match.group(1))
        return float('inf')

    def update(self, dt):
        """Actualiza el sprite y animación"""
        self.frame_timer += dt
        if self.frame_timer >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.frame_timer = 0
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

    def attack(self, target):
        """Ataca a un objetivo"""
        if self.attack_cooldown <= 0:
            distance = self.pos.distance_to(target.pos if hasattr(target, 'pos') else target)
            
            if distance <= self.attack_range:
                damage = random.randint(8, 15)
                self.is_attacking = True
                self.attack_cooldown = self.attack_delay
                print(f"⚔️ {self.name} ataca! Daño: {damage}")
                return damage
        
        return 0

    def take_damage(self, damage):
        """Recibe daño"""
        self.hp = max(0, self.hp - damage)
        print(f"💔 {self.name} recibió {damage} de daño. HP: {self.hp}/{self.hp_max}")
        return self.hp <= 0

    def is_alive(self):
        """Retorna si el enemigo está vivo"""
        return self.hp > 0


class Hohen(Enemy):
    """Hohen el Oficinista - Jefe del Office"""
    
    def __init__(self, pos, sprite_dir=None):
        super().__init__(
            pos=pos,
            name="Hohen el Oficinista",
            hp=120,
            speed=80,
            sprite_dir=sprite_dir
        )
        self.attack_delay = 3
        self.attack_range = 200
        self.move_timer = 0
        self.move_interval = random.uniform(1, 2)
        print(f"✓ Boss creado: {self.name}")

    def update(self, dt):
        """Actualización especial para Hohen - SE MUEVE hacia Otto"""
        super().update(dt)
        
        # Movimiento hacia Otto
        self.move_timer += dt
        if self.move_timer >= self.move_interval:
            # Se mueve aleatoriamente (acerca/aleja)
            if random.random() < 0.6:
                # Moverse hacia la izquierda (hacia Otto)
                self.pos.x -= self.speed * dt
            else:
                # Moverse hacia la derecha (alejarse)
                self.pos.x += self.speed * dt
            
            self.move_timer = 0
            self.move_interval = random.uniform(1, 2)
        
        # Limitar movimiento para no salirse de pantalla
        if self.pos.x < 200:
            self.pos.x = 200
        if self.pos.x > 1100:
            self.pos.x = 1100

    def special_attack(self, target):
        """Ataque especial de Hohen"""
        if self.attack_cooldown <= 0:
            damage = random.randint(15, 25)
            self.is_attacking = True
            self.attack_cooldown = self.attack_delay * 1.5
            print(f"⚡ {self.name} usa ATAQUE ESPECIAL! Daño: {damage}")
            return damage
        return 0
