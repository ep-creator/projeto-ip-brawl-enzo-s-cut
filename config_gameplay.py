#Constantes de gameplay (regras, balanceamento, timings).

# --- PARTIDA ---
PONTOS_PARA_VENCER_CAMPEONATO = 3

# --- JOGADOR ---
VIDA_MAXIMA = 8
VELOCIDADE_BASE = 2
SPEED_BOOST_MAXIMO = 3
DAMAGE_BOOST_MAXIMO = 2

# Tamanho dos frames de sprite do jogador (largura, altura em pixels)
TAMANHO_FRAME_JOGADOR = (40, 60)

HITBOX_MAPA_AJUSTE_LARGURA = -53   # reduz a largura em relação ao rect do sprite
HITBOX_MAPA_ALTURA = 20            # altura fixa da hitbox de mapa (só a base do sprite)

# HITBOX DE ENTIDADES: usada para colisão com balas, outro player e itens.
HITBOX_ENTIDADE_AJUSTE = (-53, -30)  # ajuste (dx, dy) aplicado ao rect do sprite inteiro

# --- MUNIÇÃO ---
BALAS_MAXIMAS = 4
TEMPO_RECARGA_MS = 3000

# --- PROJÉTIL ---
PROJETIL_RAIO = 6
PROJETIL_VELOCIDADE = 10
PROJETIL_ALCANCE_MAXIMO = 315
PROJETIL_DANO_BASE = 1

# --- ITENS COLETÁVEIS ---
ITEM_TAMANHO = 32
ITEM_ARQUIVOS = {
    "life": "orb_vida.png",
    "damage": "orb_dano.png",
    "speed": "orb_velocidade.png",
}
ITEM_TENTATIVAS_SPAWN = 200  # quantas posições aleatórias tentar antes de desistir
ITEM_MARGEM_SPAWN = 40  # distância mínima das bordas da tela ao sortear posição