import pygame
import sys
from players import Player1, Player2
from itens import Itens
from settings import resolucao, largura, altura
from mapa import Mapa


# =====================================================================
# CLASSE GAME (Gerenciador do Jogo)
# =====================================================================
class Game:
    def __init__(self):
        pygame.init()
        


        # Configurações da Janela
        self.screen = pygame.display.set_mode(resolucao)
        pygame.display.set_caption("Meu Jogo Quadrado")
        
        # Controlar a taxa de quadros (FPS)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        
        # Instancia o Player 1 do lado esquerdo
        self.player1 = Player1(0, altura // 2)
        # Instancia o Player 2 bem no lado da tela
        self.player2 = Player2(largura, altura // 2)
        # Instancia o item
        self.cube = Itens(largura // 2, altura // 2)

        self.mapa = Mapa("assets/mapa_brawl.tmx")

    def handle_events(self):
        """Trata eventos do sistema (como fechar a janela)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Atualiza a lógica do jogo"""
        self.player1.move(self.mapa)
        self.player2.move(self.mapa)

        
        # Opcional: Impede o jogador de sair das bordas da tela
        self.player1.rect.clamp_ip(self.screen.get_rect())
        self.player2.rect.clamp_ip(self.screen.get_rect())


    def draw(self):
        """Limpa a tela e desenha os objetos atualizados"""
        self.screen.fill((30, 30, 30))  # Fundo grafite escuro

        self.mapa.draw(self.screen)
        # Desenha o cube

        self.cube.draw(self.screen)
        # Desenha o jogador
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        
        
        # Atualiza a tela de fato
        pygame.display.flip()

    def run(self):
        """Loop principal do jogo"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)  # Mantém o jogo a 60 FPS
            
        pygame.quit()
        sys.exit()