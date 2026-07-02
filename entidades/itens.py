
import pygame
import math
import os
import config_gameplay as config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Projectile:
    """Uma bala disparada por um jogador, viajando em linha reta até um alvo."""

    def __init__(self, x, y, target_x, target_y, color,
                 radius=config.PROJETIL_RAIO,
                 vel=config.PROJETIL_VELOCIDADE,
                 damage=config.PROJETIL_DANO_BASE):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.damage = damage  # dano que esta bala específica causará (já inclui boost do atirador)

        # Ponto de origem e alcance máximo — preenchidos por quem cria o projétil
        # (normalmente logo após a criação, junto com start_x/start_y/max_range/dono)
        self.start_x = x
        self.start_y = y
        self.max_range = config.PROJETIL_ALCANCE_MAXIMO
        self.dono = None  # referência ao Player que disparou (evita autocolisão)

        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

        dx = target_x - x
        dy = target_y - y
        distancia = math.hypot(dx, dy)
        if distancia == 0:
            distancia = 1  # evita divisão por zero se origem e alvo coincidirem

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
    """Um item coletável no mapa (vida, dano ou velocidade)."""

    def __init__(self, x, y, item_type):
        self.rect = pygame.Rect(x, y, config.ITEM_TAMANHO, config.ITEM_TAMANHO)
        self.type = item_type  # "life", "damage" ou "speed"

        nome_arquivo = config.ITEM_ARQUIVOS.get(item_type)
        if nome_arquivo is None:
            raise ValueError(
                f"Tipo de item desconhecido: '{item_type}'. "
                f"Tipos válidos: {list(config.ITEM_ARQUIVOS.keys())}"
            )

        caminho = os.path.join(BASE_DIR, "assets", "coletaveis", nome_arquivo)
        img_original = pygame.image.load(caminho).convert_alpha()
        self.image = pygame.transform.scale(img_original, (self.rect.width, self.rect.height))

    def draw(self, surface):
        surface.blit(self.image, self.rect)