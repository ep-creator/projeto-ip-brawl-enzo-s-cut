import pygame
import os
from settings import largura, altura
from personagens import Personagens

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def escolher_personagens(tela):
   
    clock = pygame.time.Clock()

    info_personagens = list(Personagens.keys())

    fonte_titulo = pygame.font.SysFont("nougat", 40, bold=True)
    fonte_nome = pygame.font.SysFont("nougat", 22, bold=True)
    fonte_status = pygame.font.SysFont("nougat", 22, bold=True)
    fonte_dica = pygame.font.SysFont("nougat", 16)

    card_largura, card_altura, espacamento = 130, 170, 20
    total = len(info_personagens) * card_largura + (len(info_personagens) - 1) * espacamento
    inicio_x = (largura - total) // 2
    y_card = (altura - card_altura) // 2

    cards = []
    previews = {}
    for i, chave in enumerate(info_personagens):
        dados = Personagens[chave]
        cards.append(pygame.Rect(inicio_x + i * (card_largura + espacamento), y_card, card_largura, card_altura))

        caminho = os.path.join(BASE_DIR, "assets", dados["asset_pasta"], dados["standing_file"])
        img = pygame.image.load(caminho).convert_alpha()
        previews[chave] = pygame.transform.scale(img, (64, 96))

    idx_p1 = 0
    idx_p2 = min(1, len(info_personagens) - 1)
    pronto_p1, pronto_p2 = False, False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None, None

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return None, None

                # Player 1
                if not pronto_p1:
                    if evento.key == pygame.K_a:
                        idx_p1 = (idx_p1 - 1) % len(info_personagens)
                    elif evento.key == pygame.K_d:
                        idx_p1 = (idx_p1 + 1) % len(info_personagens)
                if evento.key == pygame.K_SPACE:
                    pronto_p1 = not pronto_p1

                # Player 2
                if not pronto_p2:
                    if evento.key == pygame.K_LEFT:
                        idx_p2 = (idx_p2 - 1) % len(info_personagens)
                    elif evento.key == pygame.K_RIGHT:
                        idx_p2 = (idx_p2 + 1) % len(info_personagens)
                if evento.key == pygame.K_RETURN:
                    pronto_p2 = not pronto_p2

        if pronto_p1 and pronto_p2:
            return info_personagens[idx_p1], info_personagens[idx_p2]

        # ---------------- desenho ----------------
        tela.fill((15, 15, 20))

        titulo = fonte_titulo.render("Escolham seus brawlers!", True, (255, 255, 255))
        tela.blit(titulo, titulo.get_rect(center=(largura // 2, 45)))

        for i, chave in enumerate(info_personagens):
            dados = Personagens[chave]
            rect = cards[i]
            sel_p1 = (i == idx_p1)
            sel_p2 = (i == idx_p2)

            cor_fundo = (70, 70, 80) if (sel_p1 or sel_p2) else (45, 45, 52)
            pygame.draw.rect(tela, cor_fundo, rect, border_radius=12)

            if sel_p1:
                cor_borda = (0, 230, 120) if pronto_p1 else (60, 140, 255)
                pygame.draw.rect(tela, cor_borda, rect, width=4, border_radius=12)
            if sel_p2:
                cor_borda = (0, 230, 120) if pronto_p2 else (255, 80, 80)
                alvo = rect.inflate(-10, -10) if sel_p1 else rect
                pygame.draw.rect(tela, cor_borda, alvo, width=3, border_radius=12)

            centro_x = rect.centerx
            centro_y = rect.y + 60
            if previews[chave]:
                tela.blit(previews[chave], previews[chave].get_rect(center=(centro_x, centro_y)))
            else:
                pygame.draw.circle(tela, dados["cor_preview"], (centro_x, centro_y), 32)

            tela.blit(fonte_nome.render(dados["nome"], True, (255, 255, 255)),
                      fonte_nome.render(dados["nome"], True, (255, 255, 255)).get_rect(center=(centro_x, rect.y + 115)))

        status_p1 = "PRONTO!" if pronto_p1 else "escolhendo..."
        status_p2 = "PRONTO!" if pronto_p2 else "escolhendo..."

        texto_p1 = fonte_status.render(f"P1 ({Personagens[info_personagens[idx_p1]]['nome']}) - {status_p1}", True, (60, 140, 255))
        tela.blit(texto_p1, (30, altura - 65))

        texto_p2 = fonte_status.render(f"P2 ({Personagens[info_personagens[idx_p2]]['nome']}) - {status_p2}", True, (255, 80, 80))
        tela.blit(texto_p2, (largura - 30 - texto_p2.get_width(), altura - 65))

        dica = fonte_dica.render(
            "P1: A/D move, ESPAÇO confirma   |   P2: setas move, ENTER confirma   |   ESC cancela",
            True, (150, 150, 150)
        )
        tela.blit(dica, dica.get_rect(center=(largura // 2, altura - 25)))

        pygame.display.flip()
        clock.tick(30)