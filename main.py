import pygame
from game import Game
from settings import resolucao
from tela_inicial import mostrar_tela_inicial
from tela_selecao import escolher_personagens

def main():
    pygame.init()

    tela = pygame.display.set_mode(resolucao, pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("xama no brawl")

    iniciar = mostrar_tela_inicial(tela)

    if iniciar:

        p1_personagem, p2_personagem = escolher_personagens(tela)
 
        if p1_personagem is None or p2_personagem is None:
            pygame.quit()
            return

        meu_jogo = Game(tela, p1_personagem, p2_personagem)
        meu_jogo.run()

    pygame.quit()

if __name__ == "__main__":
    main()