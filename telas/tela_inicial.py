import pygame
from settings import largura, altura
from utils import (
    carregar_imagem, 
    calcular_escala_respiracao, 
    deve_desenhar_piscando, 
    checar_saida
)

def mostrar_tela_inicial(tela):
    clock = pygame.time.Clock()
    
    # --- CARREGAMENTO COM UTILS ---
    logo_cin = carregar_imagem("assets/telainicial/logo_cin.png", (820, 480))
    logo_brawl = carregar_imagem("assets/telainicial/logo_brawl.png", (600, 225))

    if not logo_cin or not logo_brawl:
        print("Erro: Arquivos base da logo não encontrados.")
        return False

    logo_cin_rect = logo_cin.get_rect(center=(largura//2, altura//2))

    bg_imagem = carregar_imagem("assets/telainicial/tela_inicio_background.png", (largura, altura), alpha=False)
    btn_surface = carregar_imagem("assets/telainicial/btn.png")

    # Função Helper para evitar repetição do código de fundo
    def desenhar_cenario_base():
        tela.blit(bg_imagem, (0, 0)) if bg_imagem else tela.fill((40, 40, 40))
        tela.blit(logo_cin, logo_cin_rect)

    pulou_animacao = False

    # --- ETAPA 1: FADE IN DO CIN ---
    alpha = 0
    while alpha < 255 and not pulou_animacao:
        for event in pygame.event.get():
            if checar_saida(event): return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
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

    # --- ETAPA 2: QUEDA E RICOCHETE DO BRAWL ---
    escala, velocidade_escala, gravidade, bounciness = 6.0, 0.0, 0.18, 0.55
    animacao_finalizada = False

    while not animacao_finalizada and not pulou_animacao:
        for event in pygame.event.get():
            if checar_saida(event): return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pulou_animacao = True
                
        desenhar_cenario_base()
        
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

    # --- ETAPA 3: TELA INICIAL / ESPERA ---
    tempo_animacao = 0
    contador_pisca = 0 

    while True: 
        for event in pygame.event.get():
            if checar_saida(event): return False
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: 
                # EFEITO CONFIRMAÇÃO: PISCAR RÁPIDO COM UTILS
                if btn_surface:
                    rect_btn = btn_surface.get_rect(center=(largura//2, altura - 40))
                    for i in range(36):
                        desenhar_cenario_base()
                        tela.blit(brawl_red, brawl_red.get_rect(center=(largura//2, altura//2 + 40)))
                        
                        if deve_desenhar_piscando(i, 2):
                            tela.blit(btn_surface, rect_btn)
                            
                        pygame.display.flip()
                        clock.tick(30)
                return True 
                
        desenhar_cenario_base()
        
        # Respiração da Logo COM UTILS
        escala_respira = calcular_escala_respiracao(tempo_animacao, 0.05)
        brawl_red = pygame.transform.scale(logo_brawl, (int(logo_brawl.get_width()*escala_respira), int(logo_brawl.get_height()*escala_respira)))
        tela.blit(brawl_red, brawl_red.get_rect(center=(largura//2, altura//2 + 40)))
        
        # Lógica do Botão Piscando COM UTILS
        if btn_surface:
            contador_pisca += 1
            if deve_desenhar_piscando(contador_pisca, 15):
                tela.blit(btn_surface, btn_surface.get_rect(center=(largura//2, altura - 40)))
        
        pygame.display.flip()
        tempo_animacao += 0.2
        clock.tick(30)