import pygame
import sys
from players import Player1, Player2
from itens import Itens, Projectile
from settings import resolucao, largura, altura
from mapa import Mapa

class Game:
    def __init__(self):
        pygame.init()
        
        # Configurações da Janela
        self.screen = pygame.display.set_mode(resolucao)
        pygame.display.set_caption("Meu Jogo Quadrado")
        
        # Controlar a taxa de quadros (FPS)
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.running = True
        
        # Instancia o Player 1 do lado esquerdo
        self.player1 = Player1(0, altura // 2.1)
        # Instancia o Player 2 bem no lado da tela
        self.player2 = Player2(largura -80, altura // 2.1)
        
        self.mapa = Mapa("assets/mapa_brawl.tmx")

        self.bullets = []


    def handle_events(self):
        """Trata eventos do sistema (como fechar a janela)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    nova_bala = Projectile(
                        x =self.player1.rect.centerx,
                        y =self.player1.rect.centery,
                        target_x= self.player2.rect.centerx,
                        target_y= self.player2.rect.centery,
                        color = (0, 150, 255) # bala azul para o player1
                    )
                    self.bullets.append(nova_bala)

                if event.key == pygame.K_RETURN:
                        nova_bala = Projectile(
                            x = self.player2.rect.centerx,
                            y = self.player2.rect.centery, 
                            target_x= self.player1.rect.centerx,
                            target_y= self.player1.rect.centery,
                            color= (255, 50, 50)
                        )
                        self.bullets.append(nova_bala) #bala vermelha pro player 2

    def update(self):
        """Atualiza a lógica do jogo"""
        self.player1.move(self.mapa)
        self.player2.move(self.mapa)

        
        # Opcional: Impede o jogador de sair das bordas da tela
        self.player1.hitbox.clamp_ip(self.screen.get_rect())
        self.player2.hitbox.clamp_ip(self.screen.get_rect())

        # Alinha a imagem e a hitbox
        self.player1.rect.center = self.player1.hitbox.center
        self.player2.rect.center = self.player2.hitbox.center
        for bala in self.bullets[:]: #[:] faz a iteração com a lista de balas funcionar, sem esse comando a remoção de balas no mapa fica uma confusão
            bala.move()
            bala_ativa = True

            if bala.x < 0 or bala.x > largura or bala.y <0 or bala.y > altura:
                self.bullets.remove(bala)
                bala_ativa = False
            
            if bala_ativa == True:
                for parede in self.mapa.walls:
                    if bala_ativa == True:
                        if bala.rect.colliderect(parede):
                            self.bullets.remove(bala)
                            bala_ativa = False
            
            if bala_ativa == True:
                if bala.rect.colliderect(self.player1.rect) and bala.color == (255, 50, 50): #só considera hit se a bala acertar o jogador e for da cor oposta
                    self.bullets.remove(bala)                                                #pq como a bala nasce no meio do player ela da hit no proprio jogador ent separa por cor
                    bala_ativa = False
                    #AQUI É PRA TIRAR A VIDA QUANDO ADD OS HEALTH POINTS.   
            
                elif bala.rect.colliderect(self.player2.rect) and bala.color == (0, 150, 255): 
                    self.bullets.remove(bala)                                                #pq como a bala nasce no meio do player ela da hit no proprio jogador ent separa por cor
                    bala_ativa = False
                    #AQUI É PRA TIRAR A VIDA QUANDO ADD OS HEALTH POINTS. 


    def draw(self):
        """Limpa a tela e desenha os objetos atualizados"""
        self.screen.fill((30, 30, 30))  # Fundo grafite escuro

        self.mapa.draw(self.screen)
        
        # Desenha o jogador
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        
        for bala in self.bullets:
            bala.draw(self.screen)
        
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