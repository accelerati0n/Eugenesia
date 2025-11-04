import pygame
import os
import random
from settings import WHITE, BLACK, WIDTH, HEIGHT, LEVEL3_BG
from player import Player
from enemy import Hohen

class OfficeLevel:
    """Nivel Office - Batalla contra Hohen"""
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        
        bg_path = LEVEL3_BG
        if os.path.exists(bg_path):
            try:
                bg_img = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(bg_img, (self.screen_width, self.screen_height))
                print(f"✓ Fondo Office cargado: {bg_path}")
            except Exception as e:
                print(f"❌ Error cargando fondo: {e}")
                self.background = pygame.Surface((self.screen_width, self.screen_height))
                self.background.fill((40, 40, 50))
        else:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((40, 40, 50))
        
        # ✅ AMBOS EN LA MISMA ALTURA DEL SUELO
        # Crear jugador (izquierda)
        self.player = Player((400, 400))
        self.player.hp = 100
        self.player.hp_max = 100
        self.player.pos = pygame.Vector2(280, 620)
        
        # Crear Hohen (derecha)
        hohen_sprites_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets", "sprites", "enemies", "hohen"
        )
        
        print(f"📂 Buscando sprites Hohen en: {hohen_sprites_path}")
        
        # ✅ MISMO Y QUE OTTO
        self.hohen = Hohen(
            pos=(self.screen_width - 400, 400),
            sprite_dir=hohen_sprites_path
        )
        
        # Grupo de sprites
        # self.all_sprites = pygame.sprite.Group(self.player, self.hohen)
        
        # Estado de la batalla
        self.battle_started = True
        self.battle_text = "¡Hohen el Oficinista aparece!"
        self.battle_timer = 0
        
        # Sistema de turnos
        self.player_attack_cooldown = 0
        self.hohen_attack_timer = 0
        self.hohen_attack_interval = random.uniform(2, 4)
        
        # Mensajes
        self.battle_log = []
        
        # Efectos visuales
        self.player_hit_flash = 0
        self.hohen_hit_flash = 0
        
        print("✓ Nivel Office iniciado")

    def update(self, dt):
        """Actualiza la lógica del nivel"""
        # self.all_sprites.update(dt)
        
        # Limitar movimiento horizontal de Otto
        if self.player.rect.left < 100:
            self.player.rect.left = 100
        if self.player.rect.right > self.screen_width - 450:
            self.player.rect.right = self.screen_width - 450
        
        # Actualizar posición de Hohen
        #TODO
        pos_init = (0,0,0)
        # self.hohen.rect.center = self.hohen.pos
        # self.hohen.rect.center = 
        
        if self.player_attack_cooldown > 0:
            self.player_attack_cooldown -= dt
        
        # ✅ ATAQUE CON Q - Mostrar sprites de pelea
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            if self.player_attack_cooldown <= 0 and self.hohen.is_alive():
                distance = self.player.rect.centerx - self.hohen.rect.centerx
                
                if abs(distance) < 300:
                    # Cambiar a sprite de pelea
                    if self.player.sprite_mode != "fight":
                        self.player.sprite_mode = "fight"
                        self.player.load_fight_sprites()
                        self.player.current_frame = 0
                        self.player.frame_timer = 0
                    
                    damage = random.randint(10, 20)
                    self.hohen.take_damage(damage)
                    self.player_attack_cooldown = 1
                    self.hohen_hit_flash = 0.2
                    self.battle_log.append(f"Otto ataca! Daño: {damage}")
        
        # Ataque de Hohen
        self.hohen_attack_timer += dt
        if self.hohen_attack_timer >= self.hohen_attack_interval and self.hohen.is_alive():
            if random.random() < 0.5:
                damage = self.hohen.special_attack(self.player)
            else:
                damage = self.hohen.attack(self.player)
            
            if damage > 0:
                self.player.hp -= damage
                self.player_hit_flash = 0.2
                self.player.set_damage_mode(0.3)  # ✅ Mostrar sprite de daño
                self.battle_log.append(f"Hohen ataca! Otto recibe {damage} de daño!")
            
            self.hohen_attack_timer = 0
            self.hohen_attack_interval = random.uniform(2, 4)
        
        if self.player_hit_flash > 0:
            self.player_hit_flash -= dt
        if self.hohen_hit_flash > 0:
            self.hohen_hit_flash -= dt
        
        if len(self.battle_log) > 5:
            self.battle_log.pop(0)
        
        if self.hohen.hp <= 0:
            print("✓ ¡Victoria!")
            return "victory"
        
        if self.player.hp <= 0:
            print("✗ ¡Derrota!")
            return "defeat"
        
        return None

    def draw(self):
        """Dibuja el nivel"""
        self.screen.blit(self.background, (0, 0))
        
        # Dibujar Otto
        if self.player_hit_flash > 0:
            player_surface = self.player.image.copy()
            white_surface = pygame.Surface(player_surface.get_size())
            white_surface.fill(WHITE)
            white_surface.set_alpha(int(255 * (self.player_hit_flash / 0.2)))
            player_surface.blit(white_surface, (0, 0))
            self.screen.blit(player_surface, self.player.rect)
        else:
            self.screen.blit(self.player.image, self.player.rect)
        
        # Dibujar Hohen
        if self.hohen_hit_flash > 0:
            hohen_surface = self.hohen.image.copy()
            white_surface = pygame.Surface(hohen_surface.get_size())
            white_surface.fill(WHITE)
            white_surface.set_alpha(int(255 * (self.hohen_hit_flash / 0.2)))
            hohen_surface.blit(white_surface, (0, 0))
            self.screen.blit(hohen_surface, self.hohen.rect)
        else:
            self.screen.blit(self.hohen.image, self.hohen.rect)
        
        # Nombres
        font = pygame.font.Font(None, 20)
        otto_name = font.render("Otto", True, WHITE)
        hohen_name = font.render("Hohen", True, WHITE)
        self.screen.blit(otto_name, (self.player.rect.centerx - 20, self.player.rect.top - 30))
        self.screen.blit(hohen_name, (self.hohen.rect.centerx - 30, self.hohen.rect.top - 30))
        
        self._draw_health_bars()
        
        if self.battle_timer < 3:
            text = pygame.font.Font(None, 36).render(self.battle_text, True, (255, 200, 0))
            text_rect = text.get_rect(center=(self.screen_width // 2, 50))
            
            bg_rect = text_rect.inflate(40, 20)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 200))
            self.screen.blit(bg_surface, bg_rect)
            
            self.screen.blit(text, text_rect)
            self.battle_timer += 0.016
        
        self._draw_battle_log()
        
        controls_text = font.render("A/D: Mover | Q: Atacar", True, (200, 200, 200))
        self.screen.blit(controls_text, (10, self.screen_height - 30))

    def _draw_health_bars(self):
        """Dibuja las barras de vida"""
        font = pygame.font.Font(None, 16)
        
        bar_width = 200
        bar_height = 20
        bar_x = 20
        bar_y = 20
        
        pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        if self.player.hp_max > 0:
            hp_percentage = max(0, self.player.hp / self.player.hp_max)
            pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, bar_width * hp_percentage, bar_height))
        
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        player_text = font.render(f"Otto: {int(self.player.hp)}/{int(self.player.hp_max)}", True, WHITE)
        self.screen.blit(player_text, (bar_x, bar_y - 25))
        
        enemy_bar_x = self.screen_width - bar_width - 20
        
        pygame.draw.rect(self.screen, (255, 0, 0), (enemy_bar_x, bar_y, bar_width, bar_height))
        
        if self.hohen.hp_max > 0:
            hp_percentage = max(0, self.hohen.hp / self.hohen.hp_max)
            pygame.draw.rect(self.screen, (255, 165, 0), (enemy_bar_x, bar_y, bar_width * hp_percentage, bar_height))
        
        pygame.draw.rect(self.screen, WHITE, (enemy_bar_x, bar_y, bar_width, bar_height), 2)
        
        enemy_text = font.render(f"Hohen: {int(self.hohen.hp)}/{int(self.hohen.hp_max)}", True, WHITE)
        self.screen.blit(enemy_text, (enemy_bar_x - 50, bar_y - 25))

    def _draw_battle_log(self):
        """Dibuja el log de batalla"""
        font = pygame.font.Font(None, 14)
        log_x = 20
        log_y = self.screen_height - 100
        
        log_height = len(self.battle_log) * 20 + 10
        log_bg = pygame.Surface((400, log_height), pygame.SRCALPHA)
        log_bg.fill((0, 0, 0, 150))
        self.screen.blit(log_bg, (log_x, log_y - log_height))
        
        for i, message in enumerate(self.battle_log):
            text = font.render(message, True, (200, 200, 200))
            self.screen.blit(text, (log_x + 5, log_y - log_height + 5 + i * 20))
