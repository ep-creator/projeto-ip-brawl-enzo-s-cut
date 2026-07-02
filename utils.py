import pygame
import os
import math

#Carrega uma imagem com segurança, converte e redimensiona se necessário.
#Retorna a superfície da imagem ou None se o arquivo não existir.
def carregar_imagem(caminho, tamanho=None, alpha=True):
    if not os.path.exists(caminho):
        print(f"Aviso: Imagem não encontrada em -> {caminho}")
        return None

    img = pygame.image.load(caminho)
    img = img.convert_alpha() if alpha else img.convert()

    if tamanho:
        img = pygame.transform.scale(img, tamanho)

    return img

#Gera um fator de escala suave que sobe e desce usando função seno.
#Ideal para fazer imagens 'respirarem' ou pulsarem na tela.
def calcular_escala_respiracao(tempo_ou_ticks, amplitude, velocidade=1.0, base=1.0):
    return base + math.sin(tempo_ou_ticks * velocidade) * amplitude

#Retorna True ou False alternadamente com base em um contador de frames.
#Útil para fazer textos, botões ou cursores piscarem no ritmo certo.
def deve_desenhar_piscando(contador_frames, intervalo_frames):
    return (contador_frames // intervalo_frames) % 2 == 0

#Verifica se o usuário tentou fechar o jogo (clicou no X ou apertou ESC).
#Retorna True se for para sair, False caso contrário.
def checar_saida(evento):
    if evento.type == pygame.QUIT:
        return True
    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
        return True
    return False

#Desenha um texto com uma borda (outline) ao redor.
#Garante que o texto fique legível independente da cor do fundo.
def desenhar_texto_contornado(tela, texto, fonte, cor_texto, cor_contorno, x, y):
    deslocamentos = [(-2, -2), (0, -2), (2, -2), (-2, 0), (2, 0), (-2, 2), (0, 2), (2, 2)]

    # Renderiza a borda UMA vez e reaproveita a mesma superfície nos 8 deslocamentos
    # (antes, fonte.render() era chamado 8x com o mesmo resultado — desperdício de CPU)
    surf_borda = fonte.render(texto, True, cor_contorno)
    for dx, dy in deslocamentos:
        tela.blit(surf_borda, surf_borda.get_rect(center=(x + dx, y + dy)))

    surf_texto = fonte.render(texto, True, cor_texto)
    tela.blit(surf_texto, surf_texto.get_rect(center=(x, y)))