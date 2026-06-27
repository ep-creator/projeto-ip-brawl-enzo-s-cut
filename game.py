import pygame
import sys
import random
import math
from players import Player1, Player2
from itens import Item, Projectile 
from settings import largura, altura
from mapa import Mapa

class Game:
    def __init__(self,tela):
        pygame.init()
        
        self.screen = tela
        pygame.display.set_caption("Meu Jogo Quadrado")

        self.clock = pygame.time.Clock()
        self.fps = 30
        self.running = True
        
        self.player1 = Player1(-1, 205)
        self.player2 = Player2(760, 205)
        
        self.mapa = Mapa("assets/mapa_brawl.tmx")

        self.bullets = []
        self.items = [] 
        
        # --- Sistema de Placar e Estados de Jogo ---
        self.p1_score = 0
        self.p2_score = 0
        self.game_over = False
        self.round_over = False       # Novo: Controla se a rodada atual terminou
        self.winner_text = ""
        self.round_winner_text = ""   # Novo: Guarda o texto do vencedor da rodada

        self.balas_p1 = 4
        self.balas_p2 = 4
        self.recarga_p1 = 0
        self.recarga_p2 = 0
        self.tempo_recarga = 3000
        
        self.spawn_inicial_itens()

    def spawn_item_seguro(self, tipo_item):
        """
        Define uma posição aleatória e segura para o surgimento (spawn) de um item,
        garantindo a ausência de sobreposição com o cenário E com outros itens ativos.
        """
        tentativas = 0
        item_posicionado = False 
        
        while tentativas < 200 and not item_posicionado:
            x = random.randint(40, largura - 40)
            y = random.randint(40, altura - 40)
            
            novo_item = Item(x, y, tipo_item)
            
            colisao_parede = novo_item.rect.collidelist(self.mapa.walls) != -1
            colisao_agua = novo_item.rect.collidelist(self.mapa.waters) != -1
            colisao_arbusto = novo_item.rect.collidelist(self.mapa.bushes) != -1
            
            # SOLUÇÃO DO BUG: Mapeia os retângulos dos itens existentes e checa se há colisão
            lista_retangulos_itens = [item.rect for item in self.items]
            colisao_item = novo_item.rect.collidelist(lista_retangulos_itens) != -1
            
            # Só posiciona se estiver livre de paredes, água, arbustos E de outros busters
            if not colisao_parede and not colisao_agua and not colisao_arbusto and not colisao_item:
                self.items.append(novo_item)
                item_posicionado = True 
                
            tentativas += 1

    def spawn_inicial_itens(self):
        self.items.clear()
        self.spawn_item_seguro("life")
        self.spawn_item_seguro("damage")
        self.spawn_item_seguro("speed")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
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
                    if event.key == pygame.K_SPACE and self.balas_p1 > 0:
                        nova_bala = Projectile(
                            x=self.player1.rect.centerx,
                            y=self.player1.rect.centery,
                            target_x=self.player2.rect.centerx,
                            target_y=self.player2.rect.centery,
                            color=(0, 150, 255),
                            damage=1 + self.player1.damage_boost
                        )
                        nova_bala.start_x = self.player1.rect.centerx
                        nova_bala.start_y = self.player1.rect.centery
                        nova_bala.max_range = 220    #define o alcance/range das balas 

                        self.bullets.append(nova_bala)
                        self.balas_p1 -= 1
                        if self.balas_p1 == 0:
                            self.recarga_p1 = pygame.time.get_ticks() # Tempo para iniciar a recarga do Player 1

                    if event.key == pygame.K_RETURN and self.balas_p2 > 0:
                        nova_bala = Projectile(
                            x=self.player2.rect.centerx,
                            y=self.player2.rect.centery,
                            target_x=self.player1.rect.centerx,
                            target_y=self.player1.rect.centery,
                            color=(255, 50, 50),
                            damage=1 + self.player2.damage_boost
                        )
                        nova_bala.start_x = self.player2.rect.centerx
                        nova_bala.start_y = self.player2.rect.centery
                        nova_bala.max_range = 220    

                        self.bullets.append(nova_bala)
                        self.balas_p2 -= 1
                        if self.balas_p2 == 0:
                            self.recarga_p2 = pygame.time.get_ticks() # Tempo para iniciar a recarga do Player 2

    def checar_bala(self, bala):
        dist_percorrida = math.hypot(bala.x - bala.start_x, bala.y - bala.start_y)
        if dist_percorrida > bala.max_range:
            return True

        if bala.x < 0 or bala.x > largura or bala.y < 0 or bala.y > altura:
            return True

        if any(bala.rect.colliderect(parede) for parede in self.mapa.walls):
            return True

        # Bala vermelha acertou o Player 1
        if bala.color == (255, 50, 50) and bala.rect.colliderect(self.player1.hitbox):
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
        if bala.color == (0, 150, 255) and bala.rect.colliderect(self.player2.hitbox):
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
        self.balas_p1 = 4
        self.balas_p2 = 4
        self.recarga_p1 = 0
        self.recarga_p2 = 0

    def aplicar_coleta(self, player, item):
        if item.type == "life":
            if player.vida < 7:
                player.vida += 1
        elif item.type == "damage":
            if player.damage_boost < 2:
                player.damage_boost += 1
        elif item.type == "speed":
            if player.speed_boost < 3:
                player.speed_boost += 1

    def update(self):
        # Trava os updates se a rodada ou o jogo tiverem acabado
        if not self.game_over and not self.round_over:

            atual_time = pygame.time.get_ticks()
            if self.balas_p1 == 0 and atual_time - self.recarga_p1 >= self.tempo_recarga:
                self.balas_p1 = 4
                self.recarga_p1 = 0
            if self.balas_p2 == 0 and atual_time - self.recarga_p2 >= self.tempo_recarga:
                self.balas_p2 = 4
                self.recarga_p2 = 0

            self.player1.move(self.mapa)
            self.player2.move(self.mapa)

            self.player1.hitbox.clamp_ip(self.screen.get_rect())
            self.player2.hitbox.clamp_ip(self.screen.get_rect())

            self.player1.rect.center = self.player1.hitbox.center
            self.player2.rect.center = self.player2.hitbox.center
            
            for bala in self.bullets[:]: 
                bala.move()

            for item in self.items[:]:
                if self.player1.hitbox.colliderect(item.rect):
                    self.aplicar_coleta(self.player1, item)
                    self.items.remove(item)
                    self.spawn_item_seguro(item.type) 
                elif self.player2.hitbox.colliderect(item.rect):
                    self.aplicar_coleta(self.player2, item)
                    self.items.remove(item)
                    self.spawn_item_seguro(item.type) 

            balas_para_remover = [bala for bala in self.bullets if self.checar_bala(bala)]
            for bala in balas_para_remover:
                if bala in self.bullets: 
                    self.bullets.remove(bala)

    def draw(self):
        self.screen.fill((30, 30, 30)) 
        self.mapa.draw(self.screen)
        
        for item in self.items:
            item.draw(self.screen)

        self.player1.draw(self.screen)
        self.player2.draw(self.screen)

        for bala in self.bullets:
            bala.draw(self.screen)

        self.player1.draw_hud(self.screen, label_x=10, label_y=10)
        self.player2.draw_hud(self.screen, label_x=largura - 130, label_y=10)

        # Placar Central Superior
        font_placar = pygame.font.SysFont(None, 32, bold=True)
        texto_placar = f"{self.p1_score}  X  {self.p2_score}"
        label_placar = font_placar.render(texto_placar, True, (255, 215, 0)) 
        pos_x_placar = (largura - label_placar.get_width()) // 2
        self.screen.blit(label_placar, (pos_x_placar, 10))

        # --- TELA DE FIM DE RODADA ---
        if self.round_over and not self.game_over:
            overlay_round = pygame.Surface((largura, altura))
            overlay_round.set_alpha(160)
            overlay_round.fill((10, 10, 20))
            self.screen.blit(overlay_round, (0, 0))

            font_rodada = pygame.font.SysFont(None, 42, bold=True)
            label_rodada = font_rodada.render(self.round_winner_text, True, (255, 140, 0)) # Laranja Alerta
            pos_x_rod = (largura - label_rodada.get_width()) // 2
            pos_y_rod = (altura - label_rodada.get_height()) // 2 - 20
            self.screen.blit(label_rodada, (pos_x_rod, pos_y_rod))

            font_continua = pygame.font.SysFont(None, 22)
            label_continua = font_continua.render("Pressione ESPAÇO para o próximo round", True, (255, 255, 255))
            pos_x_cont = (largura - label_continua.get_width()) // 2
            self.screen.blit(label_continua, (pos_x_cont, pos_y_rod + 50))

        # --- TELA DE FIM DE JOGO (MD3 CONCLUÍDA) ---
        if self.game_over:
            overlay_game = pygame.Surface((largura, altura))
            overlay_game.set_alpha(200)
            overlay_game.fill((0, 0, 0))
            self.screen.blit(overlay_game, (0, 0))

            font_vitoria = pygame.font.SysFont(None, 46, bold=True)
            label_vitoria = font_vitoria.render(self.winner_text, True, (0, 255, 128))
            pos_x_vit = (largura - label_vitoria.get_width()) // 2
            pos_y_vit = (altura - label_vitoria.get_height()) // 2 - 20
            self.screen.blit(label_vitoria, (pos_x_vit, pos_y_vit))

            font_restart = pygame.font.SysFont(None, 22)
            label_restart = font_restart.render("Pressione 'R' para reiniciar o campeonato", True, (255, 255, 255))
            pos_x_res = (largura - label_restart.get_width()) // 2
            self.screen.blit(label_restart, (pos_x_res, pos_y_vit + 50))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()