import pygame
import os
import math
from settings import largura, altura

def mostrar_tela_inicial(tela):
    clock = pygame.time.Clock()
    
    # --- CARREGANDO TODOS OS ARQUIVOS LOGO NO INÍCIO ---
    caminho_cin = "assets/telainicial/logo_cin.png"
    caminho_brawl = "assets/telainicial/logo_brawl.png"
    caminho_imagem = "assets/telainicial/tela_inicio_background.png"
    caminho_btn = "assets/telainicial/btn.png" # Agora apenas um único sprite
    
    if os.path.exists(caminho_cin) and os.path.exists(caminho_brawl):
        logo_cin = pygame.image.load(caminho_cin).convert_alpha()
        logo_brawl = pygame.image.load(caminho_brawl).convert_alpha()

        logo_cin = pygame.transform.scale(logo_cin, (820, 480))
        logo_brawl = pygame.transform.scale(logo_brawl, (600, 225))

        logo_cin_rect = logo_cin.get_rect(center=(largura//2, altura//2))
    else:
        return False

    imagem_scaled = None
    if os.path.exists(caminho_imagem):
        imagem_original = pygame.image.load(caminho_imagem).convert()
        imagem_scaled = pygame.transform.scale(imagem_original, (largura, altura))
        
    btn_surface = None
    if os.path.exists(caminho_btn):
        btn_surface = pygame.image.load(caminho_btn).convert_alpha()
    
    pulou_animacao = False
    contador_pisca = 0 

    # --- ETAPA 1: FADE IN DO CIN (Fundo Preto) ---
    alpha = 0
    while alpha < 255 and not pulou_animacao:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE: 
                    pulou_animacao = True
        
        tela.fill((0, 0, 0)) 
        logo_cin.set_alpha(alpha)
        tela.blit(logo_cin, logo_cin_rect)
        pygame.display.flip()
        alpha += 5
        clock.tick(30)
        
    logo_cin.set_alpha(255)
        
    if not pulou_animacao:
        pygame.time.delay(300)

    # --- ETAPA 2: QUEDA E RICOCHETE DO BRAWL (Fundo Normal + CIn) ---
    if not pulou_animacao:
        escala = 6.0
        velocidade_escala = 0.0
        gravidade = 0.18
        bounciness = 0.55
        animacao_finalizada = False
        
        while not animacao_finalizada and not pulou_animacao:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return False
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE: 
                        pulou_animacao = True
            
            if imagem_scaled:
                tela.blit(imagem_scaled, (0, 0))
            else:
                tela.fill((40, 40, 40))
                
            tela.blit(logo_cin, logo_cin_rect)
            
            velocidade_escala += gravidade
            escala -= velocidade_escala
            
            if escala <= 1.0:
                escala = 1.0
                velocidade_escala = -velocidade_escala * bounciness
                if abs(velocidade_escala) < 0.05: animacao_finalizada = True
            
            brawl_red = pygame.transform.scale(logo_brawl, (int(logo_brawl.get_width()*escala), int(logo_brawl.get_height()*escala)))
            tela.blit(brawl_red, brawl_red.get_rect(center=(largura//2, altura//2 + 40)))
            pygame.display.flip()
            clock.tick(30)

    # --- ETAPA 3: TELA INICIAL / ESPERA (Respiração + Botão Piscando) ---
    tempo_animacao = 0
    aguardando = True
    
    while aguardando: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    # --- EFEITO CONFIRMAÇÃO: PISCAR SUPER RÁPIDO ---
                    if btn_surface:
                        rect_btn = btn_surface.get_rect(center=(largura//2, altura - 40))
                        # Loop de 12 frames (~0.4 segundos) para o flash rápido
                        for i in range(36):
                            if imagem_scaled: tela.blit(imagem_scaled, (0, 0))
                            else: tela.fill((40, 40, 40))
                            
                            tela.blit(logo_cin, logo_cin_rect)
                            tela.blit(brawl_red, brawl_red.get_rect(center=(largura//2, altura//2 + 40)))
                            
                            # Alterna visibilidade a cada 2 frames (efeito estroboscópico rápido)
                            if (i // 2) % 2 == 0:
                                tela.blit(btn_surface, rect_btn)
                                
                            pygame.display.flip()
                            clock.tick(30)
                    return True # Transiciona para a tela de seleção
                    
                if event.key == pygame.K_ESCAPE: 
                    return False 
        
        if imagem_scaled:
            tela.blit(imagem_scaled, (0, 0))
        else:
            tela.fill((40, 40, 40))
            
        tela.blit(logo_cin, logo_cin_rect)
        
        escala_respira = 1.0 + (math.sin(tempo_animacao) * 0.05)
        brawl_red = pygame.transform.scale(logo_brawl, (int(logo_brawl.get_width()*escala_respira), int(logo_brawl.get_height()*escala_respira)))
        tela.blit(brawl_red, brawl_red.get_rect(center=(largura//2, altura//2 + 40)))
        
        # --- LÓGICA DO BOTÃO PISCANDO (1 SEGUNDO TOTAL) ---
        if btn_surface:
            contador_pisca += 1
            rect_btn = btn_surface.get_rect(center=(largura//2, altura - 40)) 
            # 15 frames visível + 15 frames invisível = 30 frames (1 segundo cravado)
            if (contador_pisca // 15) % 2 == 0:
                tela.blit(btn_surface, rect_btn)
        
        pygame.display.flip()
        tempo_animacao += 0.1
        clock.tick(30)