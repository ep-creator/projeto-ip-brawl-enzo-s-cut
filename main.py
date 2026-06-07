import pygame
from game import *
from settings import resolucao


def main():
    pygame.init()

    tela = pygame.display.set_mode(resolucao)

    pygame.display.set_caption("xama no brawl")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        tela.fill((0,0,0))

        pygame.display.flip()

    pygame.QUIT()

if __name__ == "__main__":
    main()