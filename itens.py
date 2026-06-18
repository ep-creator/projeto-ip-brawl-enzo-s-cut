import pygame
import math 

class Projectile():
    # Adicionado parâmetro 'damage' para computar o boost do jogador
    def __init__(self, x, y, target_x, target_y, radius=6, color=(0,0,0), vel=10, damage=1):
        self.x = x
        self.y = y
        self.radius = radius 
        self.color = color
        self.damage = damage # Guarda o dano que essa bala específica causará
        
        dx = target_x - x
        dy = target_y - y

        distancia = math.hypot(dx, dy)

        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        if distancia == 0:
            distancia = 1   
        
        self.vel_x = (dx / distancia) * vel
        self.vel_y = (dy / distancia) * vel 

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y 

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y) 

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)

class Item:
    def __init__(self, x, y, item_type):
        # Tamanho 25x25 para ficar bem visível no mapa
        self.rect = pygame.Rect(x, y, 25, 25)
        self.type = item_type  # "life", "damage", "speed"

        if item_type == "life":
            self.color = (0, 255, 100)    # Verde claro / Vida
        elif item_type == "damage":
            self.color = (255, 128, 0)    # Laranja / Força
        elif item_type == "speed":
            self.color = (0, 191, 255)    # Azul Ciano / Velocidade

    def draw(self, surface):
        # Desenha o quadrado preenchido
        pygame.draw.rect(surface, self.color, self.rect)
        # Desenha uma borda preta fina para dar contraste
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        # Desenha um detalhe interno para identificar visualmente o item
        font = pygame.font.SysFont(None, 22, bold=True)
        simbolo = "H" if self.type == "life" else ("D" if self.type == "damage" else "S")
        texto = font.render(simbolo, True, (255, 255, 255))
        pos_texto = texto.get_rect(center=self.rect.center)
        surface.blit(texto, pos_texto)