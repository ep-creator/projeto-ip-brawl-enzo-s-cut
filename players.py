import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Player:
    def __init__(self, x, y, image, controls):
        
        def carregar_frame(nome_arquivo, prop1=30, prop2=60):
            caminho = os.path.join(BASE_DIR, "assets/shelly", nome_arquivo)
            img = pygame.image.load(caminho).convert_alpha()
            return pygame.transform.scale(img, (prop1, prop2))
        
        self.walkleft = [carregar_frame('L1.png'), carregar_frame('L2.png')]
        self.walkright = [carregar_frame('R1.png'), carregar_frame('R2.png')]
        self.walkup = [carregar_frame('U1.png'), carregar_frame('U2.png')]
        self.walkdown = [carregar_frame('B1.png'), carregar_frame('B2.png')]
        self.standing = carregar_frame('shelly.png', 65, 60)

        self.rect = self.standing.get_rect()
        self.rect.topleft = (x, y)
        self.hitbox = self.rect.inflate(-53, -20)

        self.speed_base = 2
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
        self.vida_max = 5
        self.vida = self.vida_max

    def move(self, mapa):
        old_x = self.hitbox.x
        old_y = self.hitbox.y

        keys = pygame.key.get_pressed()
        velocidade_atual = self.speed_base + self.speed_boost

        if keys[self.controls["left"]]:
            self.hitbox.x -= velocidade_atual
            self.left = True
            self.right = False
        elif keys[self.controls["right"]]:
            self.hitbox.x += velocidade_atual
            self.right = True
            self.left = False
        else:
            self.left = False
            self.right = False

        colisao_x = False
        for wall in mapa.walls:
            if self.hitbox.colliderect(wall):
                colisao_x = True
               
        for water in mapa.waters:
            if self.hitbox.colliderect(water):
                colisao_x = True

        if colisao_x:
            self.hitbox.x = old_x

        if keys[self.controls["up"]]:
            self.hitbox.y -= velocidade_atual
            self.up = True
            self.down = False
        elif keys[self.controls["down"]]:
            self.hitbox.y += velocidade_atual
            self.down = True
            self.up = False
        else:
            self.up, self.down = False, False

        colisao_y = False
        for wall in mapa.walls:
            if self.hitbox.colliderect(wall):
                colisao_y = True
                
        for water in mapa.waters:
            if self.hitbox.colliderect(water):
                colisao_y = True

        if colisao_y:
            self.hitbox.y = old_y

        self.hidden = False
        area_player = self.hitbox.width * self.hitbox.height

        for bush in mapa.bushes:
            if self.hitbox.colliderect(bush):
                intersecao = self.hitbox.clip(bush)
                area_no_arbusto = intersecao.width * intersecao.height

                if area_no_arbusto >= (area_player/2):
                    self.hidden = True

        self.rect.center = self.hitbox.center

    def draw(self, surface):
        if self.walkcount + 1 > 30:
            self.walkcount = 0

        if self.hidden:
            return

        if self.left:
            sprite_atual = self.walkleft[self.walkcount // 15]
            self.walkcount += 1
        elif self.right:
            sprite_atual = self.walkright[self.walkcount // 15]
            self.walkcount += 1
        elif self.up:
            sprite_atual = self.walkup[self.walkcount // 15]
            self.walkcount += 1
        elif self.down:
            sprite_atual = self.walkdown[self.walkcount // 15]
            self.walkcount += 1
        else:
            sprite_atual = self.standing
            self.walkcount = 0

        posicao_alinhada = sprite_atual.get_rect(midbottom=self.rect.midbottom)
        surface.blit(sprite_atual, posicao_alinhada)

    def draw_hud(self, surface, label_x, label_y):
        font = pygame.font.SysFont(None, 20)
        font_stats = pygame.font.SysFont(None, 16)
        
        label = font.render(f"P{self.player_num}", True, self.color)
        heart_size = 12
        gap = 4
        
        total_quadrados = max(self.vida_max, self.vida)

        if self.player_num == 1:
            surface.blit(label, (label_x, label_y))
            for i in range(total_quadrados):
                x = label_x + 28 + i * (heart_size + gap)
                if i < self.vida:
                    cor_vida = (0, 255, 0) if i >= self.vida_max else self.color
                else:
                    cor_vida = (80, 80, 80)
                pygame.draw.rect(surface, cor_vida, (x, label_y, heart_size, heart_size))

            texto_stats = f"Dmg: +{self.damage_boost}  Spd: +{self.speed_boost}"
            label_stats = font_stats.render(texto_stats, True, (255, 255, 255))
            surface.blit(label_stats, (label_x, label_y + 16))

        elif self.player_num == 2:
            surface.blit(label, (label_x + 110, label_y))
            for i in range(total_quadrados):
                x = label_x + 90 - i * (heart_size + gap)
                if i < self.vida:
                    cor_vida = (0, 255, 0) if i >= self.vida_max else self.color
                else:
                    cor_vida = (80, 80, 80)
                pygame.draw.rect(surface, cor_vida, (x, label_y, heart_size, heart_size))

            texto_stats = f"Dmg: +{self.damage_boost}  Spd: +{self.speed_boost}"
            label_stats = font_stats.render(texto_stats, True, (255, 255, 255))
            largura_stats = label_stats.get_width()
            surface.blit(label_stats, (label_x + 130 - largura_stats, label_y + 16))

    def damage(self, qtd_dano=1):
        self.vida -= qtd_dano
        if self.vida <= 0:
            return True  
        return False

    def respawn(self):
        self.vida = self.vida_max
        self.speed_boost = 0   
        self.damage_boost = 0  
        self.rect.topleft = (self.spawn_x, self.spawn_y)
        self.hitbox = self.rect.inflate(-53, -20)

class Player1(Player):
    def __init__(self, x, y):
        super().__init__(x, y, 'shelly.png', {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s})
        self.color = (0, 0, 255)
        self.player_num = 1

class Player2(Player):
    def __init__(self, x, y):
        super().__init__(x, y, 'shelly.png',{ "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN})
        self.color = (255, 0, 0)
        self.player_num = 2