import pygame
import os
import math
from settings import largura, altura
from personagens import Personagens

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Constantes de Cores
COR_BRANCA = (255, 255, 255)
COR_FUNDO = (15, 15, 20)
COR_P1 = (0, 255, 255)
COR_P2 = (255, 80, 80)
COR_VERDE_CONFIRM = (50, 255, 50)

def desenhar_texto_contornado(tela, texto, fonte, cor_texto, cor_contorno, x, y):
    deslocamentos = [(-2, -2), (0, -2), (2, -2), (-2, 0), (2, 0), (-2, 2), (0, 2), (2, 2)]
    for dx, dy in deslocamentos:
        surf_borda = fonte.render(texto, True, cor_contorno)
        tela.blit(surf_borda, surf_borda.get_rect(center=(x + dx, y + dy)))
    
    surf_texto = fonte.render(texto, True, cor_texto)
    tela.blit(surf_texto, surf_texto.get_rect(center=(x, y)))

def carregar_recursos_selecao():
    """Carrega e retorna fontes e imagens necessárias para a tela de seleção."""
    caminho_fonte = os.path.join(BASE_DIR, "assets", "LilitaOne-Regular.ttf")
    fonte_base = caminho_fonte if os.path.exists(caminho_fonte) else None

    fontes = {
        "titulo": pygame.font.Font(fonte_base, 42) if fonte_base else pygame.font.SysFont("Arial", 45, bold=True),
        "nome": pygame.font.Font(fonte_base, 36) if fonte_base else pygame.font.SysFont("Arial", 36, bold=True),
        "setas": pygame.font.Font(fonte_base, 60) if fonte_base else pygame.font.SysFont("Arial", 60, bold=True)
    }

    caminho_bg = os.path.join(BASE_DIR, "assets", "telaselecao", "background.png")
    fundo_img = pygame.transform.scale(pygame.image.load(caminho_bg).convert(), (largura, altura)) if os.path.exists(caminho_bg) else None
    
    caminho_titulo = os.path.join(BASE_DIR, "assets", "telaselecao", "escolham_brawlers.png")
    titulo_img = None
    if os.path.exists(caminho_titulo):
        img_t = pygame.image.load(caminho_titulo).convert_alpha()
        titulo_img = pygame.transform.scale(img_t, (int(img_t.get_width()*0.8), int(img_t.get_height()*0.8)))

    sprites = {}
    for chave, dados in Personagens.items():
        caminho_sprite = os.path.join(BASE_DIR, "assets", dados["asset_pasta"], dados["standing_file"])
        if os.path.exists(caminho_sprite):
            img = pygame.image.load(caminho_sprite).convert_alpha()
            fator = 220 / img.get_height()
            sprites[chave] = pygame.transform.scale(img, (int(img.get_width() * fator), 220))

    return fontes, fundo_img, titulo_img, sprites

def escolher_personagens(tela):
    clock = pygame.time.Clock()
    info_personagens = list(Personagens.keys())
    fontes, fundo_img, titulo_img, sprites = carregar_recursos_selecao()

    # Dicionário organizando o estado de cada jogador (Clean Code)
    jogadores = {
        "P1": {"idx": 0, "status": 0, "conf": False, "cx": largura // 4, "cor": COR_P1, "teclas": (pygame.K_a, pygame.K_d, pygame.K_SPACE)},
        "P2": {"idx": min(1, len(info_personagens) - 1), "status": 0, "conf": False, "cx": (3 * largura) // 4, "cor": COR_P2, "teclas": (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN)}
    }

    while True:
        # --- EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                return None, None
            
            if evento.type == pygame.KEYDOWN:
                for j_id, j in jogadores.items():
                    k_esq, k_dir, k_acao = j["teclas"]
                    
                    if evento.key == k_acao:
                        if j["conf"]:  # Cancelar confirmação
                            j["conf"], j["status"] = False, 0
                        elif j["status"] == 0:  # Iniciar animação de confirmar
                            j["status"] = 30
                    
                    elif j["status"] == 0 and not j["conf"]:
                        if evento.key == k_esq:
                            j["idx"] = (j["idx"] - 1) % len(info_personagens)
                        elif evento.key == k_dir:
                            j["idx"] = (j["idx"] + 1) % len(info_personagens)

        # --- ATUALIZAÇÃO DE LÓGICA ---
        for j in jogadores.values():
            if j["status"] > 0:
                j["status"] -= 1
                if j["status"] == 0:
                    j["conf"] = True

        if jogadores["P1"]["conf"] and jogadores["P2"]["conf"]:
            return info_personagens[jogadores["P1"]["idx"]], info_personagens[jogadores["P2"]["idx"]]

        # --- DESENHO ---
        tela.blit(fundo_img, (0, 0)) if fundo_img else tela.fill(COR_FUNDO)

        # Título Animado
        if titulo_img:
            f = 1.0 + math.sin(pygame.time.get_ticks() * 0.004) * 0.04
            t_an = pygame.transform.scale(titulo_img, (int(titulo_img.get_width()*f), int(titulo_img.get_height()*f)))
            tela.blit(t_an, t_an.get_rect(center=(largura // 2, 50)))

        desenhar_texto_contornado(tela, "PLAYER 1", fontes["titulo"], COR_BRANCA, COR_P1, jogadores["P1"]["cx"], 160)
        desenhar_texto_contornado(tela, "PLAYER 2", fontes["titulo"], COR_BRANCA, COR_P2, jogadores["P2"]["cx"], 160)

        # Desenhar Personagens e UI (Loop unificado)
        y_c = 295
        for i, (j_id, j) in enumerate(jogadores.items()):
            # Piscar durante confirmação
            if not (j["status"] > 0 and (j["status"] % 4 < 2)):
                if not j["conf"]:
                    seta_esq = fontes["setas"].render("<", True, j["cor"])
                    seta_dir = fontes["setas"].render(">", True, j["cor"])
                    tela.blit(seta_esq, seta_esq.get_rect(center=(j["cx"] - 120, y_c)))
                    tela.blit(seta_dir, seta_dir.get_rect(center=(j["cx"] + 120, y_c)))
                
                chave_pers = info_personagens[j["idx"]]
                if chave_pers in sprites:
                    sprite = sprites[chave_pers]
                    if j_id == "P2": 
                        sprite = pygame.transform.flip(sprite, True, False)
                    tela.blit(sprite, sprite.get_rect(center=(j["cx"], y_c)))
                
                cor_nome = COR_VERDE_CONFIRM if j["conf"] else COR_BRANCA
                nome_surf = fontes["nome"].render(Personagens[chave_pers]["nome"], True, cor_nome)
                tela.blit(nome_surf, nome_surf.get_rect(center=(j["cx"], y_c + 110)))

        pygame.display.flip()
        clock.tick(30)