import pygame
from settings import WHITE, BLACK, WIDTH, HEIGHT

class DialogBox:
    """Sistema de diálogos estilo Pokémon"""
    
    def __init__(self, screen, text, title="", width=600, height=200):
        self.screen = screen
        self.text = text
        self.title = title
        self.width = width
        self.height = height
        
        self.x = (WIDTH - width) // 2
        self.y = HEIGHT - height - 50
        
        self.title_font = pygame.font.Font(None, 28)
        self.text_font = pygame.font.Font(None, 20)
        
        self.char_index = 0
        self.text_speed = 0.05
        self.char_timer = 0
        self.finished = False
        
        print(f"✓ DialogBox creado: {title}")

    def update(self, dt):
        """Actualiza la animación del texto"""
        if not self.finished:
            self.char_timer += dt * 1000
            
            if self.char_timer >= self.text_speed * 100:
                if self.char_index < len(self.text):
                    self.char_index += 1
                    self.char_timer = 0
                else:
                    self.finished = True

    def draw(self):
        """Dibuja el cuadro de diálogo"""
        bg_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 220))
        self.screen.blit(bg_surface, (self.x, self.y))
        
        pygame.draw.rect(self.screen, WHITE, (self.x, self.y, self.width, self.height), 3)
        
        if self.title:
            title_surf = self.title_font.render(self.title, True, WHITE)
            title_rect = title_surf.get_rect(topleft=(self.x + 20, self.y + 15))
            self.screen.blit(title_surf, title_rect)
            
            pygame.draw.line(
                self.screen,
                WHITE,
                (self.x + 20, self.y + 50),
                (self.x + self.width - 20, self.y + 50),
                2
            )
        
        visible_text = self.text[:self.char_index]
        lines = self._wrap_text(visible_text, self.width - 40)
        
        y_offset = self.y + 70 if self.title else self.y + 20
        for i, line in enumerate(lines):
            text_surf = self.text_font.render(line, True, WHITE)
            text_rect = text_surf.get_rect(topleft=(self.x + 20, y_offset + i * 30))
            self.screen.blit(text_surf, text_rect)
        
        if self.finished:
            indicator = "▼ Presiona ENTER para continuar"
            indicator_surf = self.text_font.render(indicator, True, (255, 255, 100))
            indicator_rect = indicator_surf.get_rect(bottomright=(self.x + self.width - 20, self.y + self.height - 10))
            self.screen.blit(indicator_surf, indicator_rect)

    def _wrap_text(self, text, max_width):
        """Envuelve el texto para que quepa en el ancho máximo"""
        lines = []
        current_line = ""
        words = text.split(" ")
        
        for word in words:
            test_line = current_line + word + " "
            text_width = self.text_font.size(test_line)[0]
            
            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines

    def is_finished(self):
        """Retorna True si el diálogo se puede avanzar"""
        return self.finished


class DialogSequence:
    """Maneja una secuencia de diálogos"""
    
    def __init__(self, screen, dialogs):
        self.screen = screen
        self.dialogs = dialogs
        self.current_index = 0
        self.current_dialog = None
        self.sequence_finished = False
        
        self._start_dialog(0)
    
    def _start_dialog(self, index):
        """Inicia un diálogo específico"""
        if index < len(self.dialogs):
            dialog_data = self.dialogs[index]
            self.current_dialog = DialogBox(
                self.screen,
                dialog_data['text'],
                dialog_data.get('title', ''),
                width=700,
                height=250
            )
        else:
            self.sequence_finished = True

    def update(self, dt):
        """Actualiza la secuencia de diálogos"""
        if self.current_dialog and not self.sequence_finished:
            self.current_dialog.update(dt)

    def handle_input(self):
        """Maneja input del usuario (ENTER para avanzar)"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            if self.current_dialog.is_finished():
                self.current_index += 1
                self._start_dialog(self.current_index)
                return True
        return False

    def draw(self):
        """Dibuja el diálogo actual"""
        if self.current_dialog:
            self.current_dialog.draw()

    def is_finished(self):
        """Retorna True si la secuencia terminó"""
        return self.sequence_finished
