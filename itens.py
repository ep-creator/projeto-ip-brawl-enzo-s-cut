import pygame
import math
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
        # Tamanho estruturado para a colisão do item no mapa 
        self.rect = pygame.Rect(x, y, 32, 32)
        self.type = item_type  # "life", "damage", "speed"

        if item_type == "life":
            nome_arquivo = "orb_vida.png"
        elif item_type == "damage":
            nome_arquivo = "orb_dano.png"
        elif item_type == "speed":
            nome_arquivo = "orb_velocidade.png"

        caminho = os.path.join(BASE_DIR, "assets", "coletaveis", nome_arquivo)
        
        img_original = pygame.image.load(caminho).convert_alpha()
        
        self.image = pygame.transform.scale(img_original, (self.rect.width, self.rect.height))

    def draw(self, surface):
        # Desenha a imagem do Orb diretamente na tela utilizando a posição do rect
        surface.blit(self.image, self.rect)