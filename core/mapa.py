import pygame
from pytmx.util_pygame import load_pygame


class Mapa:

    def __init__(self, arquivo):

        self.tmx = load_pygame(arquivo) 

        self.imagem = pygame.image.load("assets/Map (10).png").convert()

        # Cria tres listas vazias para guardar as areas do mapa que terao as regras
        self.walls = []
        self.waters = []
        self.bushes = []

        self.carregar_objetos()

    def carregar_objetos(self):

        # Organiza o mapa em camadas e percorre
        for layer in self.tmx.layers:

            if layer.name == "wall":

                for obj in layer:

                    self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            elif layer.name == "water":

                for obj in layer:

                    self.waters.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            elif layer.name == "bush":

                for obj in layer:

                    self.bushes.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def draw(self, screen):

        screen.blit(self.imagem, (0, 0))