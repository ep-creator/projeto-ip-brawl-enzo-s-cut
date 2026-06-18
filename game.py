import pygame
import sys
import random
from players import Player1, Player2
from itens import Itens, Projectile
from settings import resolucao, largura, altura
from mapa import Mapa
import random

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(resolucao)
        pygame.display.set_caption("Meu Jogo Quadrado")

        self.clock = pygame.time.Clock()
        self.fps = 30
        self.running = True
        
        self.player1 = Player1(-23, 200)
        self.player2 = Player2(745, 200)
        
        self.mapa = Mapa("assets/mapa_brawl.tmx")

        self.bullets = []


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # Caso o jogo completo tenha acabado (Melhor de 3)
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.p1_score = 0
                        self.p2_score = 0
                        self.game_over = False
                        self.winner_text = ""
                        self.reset_rodada()
                
                # Caso apenas a rodada tenha acabado
                elif self.round_over:
                    if event.key == pygame.K_SPACE:
                        self.round_over = False
                        self.round_winner_text = ""
                        self.reset_rodada()
                
                # Jogo rolando normalmente
                else:
                    if event.key == pygame.K_SPACE:
                        nova_bala = Projectile(
                            x=self.player1.rect.centerx,
                            y=self.player1.rect.centery,
                            target_x=self.player2.rect.centerx,
                            target_y=self.player2.rect.centery,
                            color=(0, 150, 255),
                            damage=1 + self.player1.damage_boost
                        )
                        self.bullets.append(nova_bala)

                    if event.key == pygame.K_RETURN:
                        nova_bala = Projectile(
                            x=self.player2.rect.centerx,
                            y=self.player2.rect.centery,
                            target_x=self.player1.rect.centerx,
                            target_y=self.player1.rect.centery,
                            color=(255, 50, 50),
                            damage=1 + self.player2.damage_boost
                        )
                        self.bullets.append(nova_bala)

    def checar_bala(self, bala):
        if bala.x < 0 or bala.x > largura or bala.y < 0 or bala.y > altura:
            return True

        if any(bala.rect.colliderect(parede) for parede in self.mapa.walls):
            return True

        # Bala vermelha acertou o Player 1
        if bala.color == (255, 50, 50) and bala.rect.colliderect(self.player1.rect):
            morreu = self.player1.damage(bala.damage) 
            if morreu:
                self.p2_score += 1 
                if self.p2_score >= 2: 
                    self.game_over = True
                    self.winner_text = "PLAYER 2 VENCEU O JOGO!"
                else:
                    self.round_over = True
                    self.round_winner_text = "PLAYER 2 VENCEU A RODADA!"
            return True

        # Bala azul acertou o Player 2
        if bala.color == (0, 150, 255) and bala.rect.colliderect(self.player2.rect):
            morreu = self.player2.damage(bala.damage) 
            if morreu:
                self.p1_score += 1 
                if self.p1_score >= 2: 
                    self.game_over = True
                    self.winner_text = "PLAYER 1 VENCEU O JOGO!"
                else:
                    self.round_over = True
                    self.round_winner_text = "PLAYER 1 VENCEU A RODADA!"
            return True

        return False

    def reset_rodada(self):
        self.player1.respawn()
        self.player2.respawn()
        self.bullets.clear()
        self.spawn_inicial_itens() 

    def aplicar_coleta(self, player, item):
        if item.type == "life":
            if player.vida < 7:
                player.vida += 1
        elif item.type == "damage":
            player.damage_boost += 1
        elif item.type == "speed":
            player.speed_boost += 1

    def update(self):
        # Trava os updates se a rodada ou o jogo tiverem acabado
        if not self.game_over and not self.round_over:
            self.player1.move(self.mapa)
            self.player2.move(self.mapa)

            self.player1.hitbox.clamp_ip(self.screen.get_rect())
            self.player2.hitbox.clamp_ip(self.screen.get_rect())

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
        self.screen.fill((30, 30, 30)) 
        self.mapa.draw(self.screen)
        
        for item in self.items:
            item.draw(self.screen)

        self.player1.draw(self.screen)
        self.player2.draw(self.screen)

        for bala in self.bullets:
            bala.draw(self.screen)
        
        # Atualiza a tela de fato
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)  # Mantém o jogo a 60 FPS
            
        pygame.quit()
        sys.exit()

    def posicion(self):
        while True:
            x = random.randint(0, largura - 20)
            y = random.randint(0, altura - 20)
            nova_posicao = pygame.Rect(x, y, 20, 20)

            colisao = False
            for parede in self.mapa.walls:
                if nova_posicao.colliderect(parede):
                    colisao = True
            for agua in self.mapa.waters:
                if nova_posicao.colliderect(agua):
                    colisao = True
            for mato in self.mapa.bushes:
                if nova_posicao.colliderect(mato):
                    colisao = True
            
            if not colisao:
                return x, y