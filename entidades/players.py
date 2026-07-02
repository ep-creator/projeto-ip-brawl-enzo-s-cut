import pygame
import os
import config_gameplay as config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Player:
    """Classe base de um jogador. Não deve ser instanciada diretamente —
    use Player1 ou Player2, que definem controles, cor e número do jogador."""

    def __init__(self, x, y, personagem, controls):
        self.personagem = personagem  # referência ao Personagem (nome, stats, assets)

        def carregar_frame(nome_arquivo):
            caminho = os.path.join(BASE_DIR, "assets", personagem.asset_pasta, nome_arquivo)
            img = pygame.image.load(caminho).convert_alpha()
            return pygame.transform.scale(img, config.TAMANHO_FRAME_JOGADOR)

        self.walkleft = [carregar_frame('L1.png'), carregar_frame('L2.png')]
        self.walkright = [carregar_frame('R1.png'), carregar_frame('R2.png')]
        self.walkup = [carregar_frame('U1.png'), carregar_frame('U2.png')]
        self.walkdown = [carregar_frame('B1.png'), carregar_frame('B2.png')]
        self.standing = carregar_frame(personagem.standing_file)

        # self.rect: usado apenas para desenho na tela (draw() posiciona o sprite por ele)
        self.rect = self.standing.get_rect()
        self.rect.topleft = (x, y)

        # hitbox_entidade: posição de colisão "real" do player (balas, outro player, itens).
        # É ela que se move a cada frame e dita a posição final de self.rect.
        self.hitbox_entidade = self.rect.inflate(*config.HITBOX_ENTIDADE_AJUSTE)

        # hitbox_mapa: faixa fina colada na base de hitbox_entidade, usada só para
        # colisão com paredes/água. Não guarda posição própria — é recalculada a
        # cada frame a partir de hitbox_entidade (ver _atualizar_hitbox_mapa).
        self.hitbox_mapa = pygame.Rect(0, 0, self.hitbox_entidade.width, config.HITBOX_MAPA_ALTURA)
        self._atualizar_hitbox_mapa()

        self.speed_boost = 0
        self.damage_boost = 0

        self.controls = controls
        self.hidden = False

        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkcount = 0

        self.spawn_x = x
        self.spawn_y = y
        self.vida = personagem.vida_maxima

        self.balas = config.BALAS_MAXIMAS

    def _atualizar_hitbox_mapa(self):
        """Recoloca a hitbox_mapa colada na base da hitbox_entidade.
        Chamado sempre que hitbox_entidade muda de posição."""
        self.hitbox_mapa.midbottom = self.hitbox_entidade.midbottom

    def _colide_com_mapa(self, mapa):
        """Verifica se a hitbox_mapa atual colide com paredes ou água.
        Vegetação (bushes) não bloqueia movimento — só ativa ocultação (ver _atualizar_ocultacao)."""
        if self.hitbox_mapa.collidelist(mapa.walls) != -1:
            return True
        if self.hitbox_mapa.collidelist(mapa.waters) != -1:
            return True
        return False

    def _atualizar_ocultacao(self, mapa):
        """Define self.hidden quando o player está suficientemente coberto por um arbusto."""
        self.hidden = False
        area_player = self.hitbox_entidade.width * self.hitbox_entidade.height

        for bush in mapa.bushes:
            if self.hitbox_entidade.colliderect(bush):
                intersecao = self.hitbox_entidade.clip(bush)
                area_no_arbusto = intersecao.width * intersecao.height
                if area_no_arbusto >= (area_player / 2):
                    self.hidden = True
                    break

    def move(self, mapa):
        velocidade_atual = self.personagem.velocidade + self.speed_boost
        keys = pygame.key.get_pressed()

        # --- Eixo X ---
        old_x = self.hitbox_entidade.x
        if keys[self.controls["left"]]:
            self.hitbox_entidade.x -= velocidade_atual
            self.left, self.right = True, False
        elif keys[self.controls["right"]]:
            self.hitbox_entidade.x += velocidade_atual
            self.right, self.left = True, False
        else:
            self.left, self.right = False, False

        self._atualizar_hitbox_mapa()
        if self._colide_com_mapa(mapa):
            self.hitbox_entidade.x = old_x
            self._atualizar_hitbox_mapa()

        # --- Eixo Y ---
        old_y = self.hitbox_entidade.y
        if keys[self.controls["up"]]:
            self.hitbox_entidade.y -= velocidade_atual
            self.up, self.down = True, False
        elif keys[self.controls["down"]]:
            self.hitbox_entidade.y += velocidade_atual
            self.down, self.up = True, False
        else:
            self.up, self.down = False, False

        self._atualizar_hitbox_mapa()
        if self._colide_com_mapa(mapa):
            self.hitbox_entidade.y = old_y
            self._atualizar_hitbox_mapa()

        self._atualizar_ocultacao(mapa)

        # self.rect (posição visual) só é atualizado depois que a colisão já foi resolvida
        self.rect.center = self.hitbox_entidade.center

    def draw(self, surface):
        if self.walkcount + 1 > 20:
            self.walkcount = 0

        if self.hidden:
            return

        direcoes = [
            (self.left, self.walkleft),
            (self.right, self.walkright),
            (self.up, self.walkup),
            (self.down, self.walkdown),
        ]
        sprite_atual = self.standing
        andando = False
        for ativo, frames in direcoes:
            if ativo:
                sprite_atual = frames[self.walkcount // 10]
                andando = True
                break

        self.walkcount = self.walkcount + 1 if andando else 0

        posicao_alinhada = sprite_atual.get_rect(midbottom=self.rect.midbottom)
        surface.blit(sprite_atual, posicao_alinhada)

        self.draw_above_head(surface)

    def draw_above_head(self, surface):
        if self.hidden:
            return

        font = pygame.font.SysFont(None, 12, bold=True)

        tamanho, gap = 5, 3
        largura_total = self.balas_maximas_para_hud * (tamanho + gap)
        start_x = self.rect.centerx - largura_total // 2
        start_y = self.rect.top - 5

        for i in range(self.balas_maximas_para_hud):
            cor = self.color if i < self.balas else (70, 70, 70)
            pygame.draw.rect(surface, cor, (start_x + i * (tamanho + gap), start_y, tamanho, tamanho), border_radius=1)

        texto = font.render(f"P{self.player_num}", True, (255, 255, 255))
        largura_fundo = texto.get_width() + 8
        altura_fundo = 12
        x = self.rect.centerx - largura_fundo // 2
        y = start_y - 15

        pygame.draw.rect(surface, self.color, (x, y, largura_fundo, altura_fundo), border_radius=1)
        surface.blit(texto, (x + 4, y + 2))

    @property
    def balas_maximas_para_hud(self):
        return config.BALAS_MAXIMAS

    def draw_hud(self, surface, label_x, label_y):
        """Desenha o HUD (nome, vida, stats). direcao_hud define se o HUD
        cresce para a direita (P1) ou para a esquerda (P2), definido nas subclasses."""
        font = pygame.font.SysFont(None, 20)
        font_stats = pygame.font.SysFont(None, 16)

        heart_size, gap = 12, 4
        total_quadrados = max(self.personagem.vida_maxima, self.vida)
        d = self.direcao_hud  # 1 para P1 (cresce p/ direita), -1 para P2 (cresce p/ esquerda)

        label_x_ajustado = label_x if d == 1 else label_x + 110
        label = font.render(f"P{self.player_num}", True, self.color)
        surface.blit(label, (label_x_ajustado, label_y))

        origem_coracoes = label_x + 28 if d == 1 else label_x + 90
        for i in range(total_quadrados):
            x = origem_coracoes + d * i * (heart_size + gap)
            if i < self.vida:
                cor_vida = (0, 255, 0) if i >= self.personagem.vida_maxima else self.color
            else:
                cor_vida = (80, 80, 80)
            pygame.draw.rect(surface, cor_vida, (x, label_y, heart_size, heart_size))

        texto_stats = f"Dmg: +{self.damage_boost}  Spd: +{self.speed_boost}"
        label_stats = font_stats.render(texto_stats, True, (255, 255, 255))
        if d == 1:
            surface.blit(label_stats, (label_x, label_y + 16))
        else:
            largura_stats = label_stats.get_width()
            surface.blit(label_stats, (label_x + 130 - largura_stats, label_y + 16))

    def damage(self, qtd_dano=1):
        """Aplica dano. Retorna True se o player morreu (vida <= 0)."""
        self.vida -= qtd_dano
        return self.vida <= 0

    def respawn(self):
        self.vida = self.personagem.vida_maxima
        self.speed_boost = 0
        self.damage_boost = 0
        self.balas = config.BALAS_MAXIMAS

        self.rect.topleft = (self.spawn_x, self.spawn_y)
        self.hitbox_entidade = self.rect.inflate(*config.HITBOX_ENTIDADE_AJUSTE)
        self.hitbox_mapa = pygame.Rect(0, 0, self.hitbox_entidade.width, config.HITBOX_MAPA_ALTURA)
        self._atualizar_hitbox_mapa()


class Player1(Player):
    direcao_hud = 1

    def __init__(self, x, y, personagem):
        controls = {
            "left": pygame.K_a, "right": pygame.K_d,
            "up": pygame.K_w, "down": pygame.K_s,
            "atirar": pygame.K_SPACE,
        }
        super().__init__(x, y, personagem, controls)
        self.color = (0, 0, 255)
        self.player_num = 1


class Player2(Player):
    direcao_hud = -1

    def __init__(self, x, y, personagem):
        controls = {
            "left": pygame.K_LEFT, "right": pygame.K_RIGHT,
            "up": pygame.K_UP, "down": pygame.K_DOWN,
            "atirar": pygame.K_RETURN,
        }
        super().__init__(x, y, personagem, controls)
        self.color = (255, 0, 0)
        self.player_num = 2