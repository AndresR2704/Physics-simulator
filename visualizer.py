import pygame

# Colors
BACKGROUND = (20, 20, 30)
PARTICLE_COLOR = (100, 180, 255)
SLIDER_BG = (100, 100, 120)
SLIDER_KNOB = (200, 200, 220)
TEXT_COLOR = (230, 230, 230)

class Slider:
    def __init__(self, x, y, width, height, initial_value, min_val=0.0, max_val=1.0, label="Slider"):
        self.rect = pygame.Rect(x, y, width, height)
        self.knob_width = 15
        self.knob_height = height + 10
        self.min_val = min_val
        self.max_val = max_val
        self.label = label
        
        # Initial knob position based on initial value
        knob_pos = x + ((initial_value - min_val) / (max_val - min_val)) * width
        self.knob_rect = pygame.Rect(knob_pos - self.knob_width//2, y - 5, 
                                    self.knob_width, self.knob_height)
        self.dragging = False
        self.value = initial_value
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            x_pos = max(self.rect.left, min(event.pos[0], self.rect.right))
            self.knob_rect.centerx = x_pos
            # Update value based on knob position
            self.value = self.min_val + (self.max_val - self.min_val) * ((x_pos - self.rect.left) / self.rect.width)
    
    def draw(self, screen, font):
        # Draw slider background
        pygame.draw.rect(screen, SLIDER_BG, self.rect)
        # Draw knob
        pygame.draw.rect(screen, SLIDER_KNOB, self.knob_rect)
        # Draw label and value
        if self.label == "Gravity" or self.label == "Damping" or self.label == "Bounciness":
            text = font.render(f"{self.label}: {self.value:.2f}", True, TEXT_COLOR)
        else:
            text = font.render(f"{self.label}: {int(self.value)}", True, TEXT_COLOR)
        screen.blit(text, (self.rect.x, self.rect.y - 25))

def draw_particles(screen, particles, radius):
    for pos in particles:
        pygame.draw.circle(screen, PARTICLE_COLOR, (int(pos[0]), int(pos[1])), int(radius))

def draw_ui(screen, font, sliders):
    for slider in sliders:
        slider.draw(screen, font)