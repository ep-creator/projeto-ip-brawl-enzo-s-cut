import pygame

class Player:
    def __init__(self, x, y, image_path, controls):

        imagem = pygame.image.load(image_path).convert_alpha()

        self.image = pygame.transform.scale(imagem, (80,76))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.hitbox = self.rect.inflate(-53, -20)
        self.speed = 1
        self.controls = controls
        self.hidden = False

    def move(self, mapa):
        old_x = self.hitbox.x
        old_y = self.hitbox.y

        keys = pygame.key.get_pressed()

        # Movimentação horizontal 
        if keys[self.controls["left"]]:
            self.hitbox.x -= self.speed
        if keys[self.controls["right"]]:
            self.hitbox.x += self.speed

        colisao_x = False
        for wall in mapa.walls: # testa colisão com paredes
            if self.hitbox.colliderect(wall):
                colisao_x = True
                break
        for water in mapa.waters: # testa colisão
            if self.hitbox.colliderect(water):
                colisao_x = True
                break

        if colisao_x:
            self.hitbox.x = old_x

        # Movimentação Vertical
        if keys[self.controls["up"]]:
            self.hitbox.y -= self.speed
        if keys[self.controls["down"]]:
            self.hitbox.y += self.speed

        colisao_y = False
        for wall in mapa.walls:
            if self.hitbox.colliderect(wall):
                colisao_y = True
                break
        for water in mapa.waters:
            if self.hitbox.colliderect(water):
                colisao_y = True
                break

        if colisao_y:
            self.hitbox.y = old_y

        # arbusto (esconder)
        self.hidden = False
        area_player = self.hitbox.width * self.hitbox.height

        for bush in mapa.bushes:
            if self.hitbox.colliderect(bush):
                intersecao = self.hitbox.clip(bush)
                area_no_arbusto = intersecao.width * intersecao.height

                if area_no_arbusto >= (area_player/2):
                    self.hidden = True
                    break

        self.rect.center = self.hitbox.center

    def draw(self, surface):
        if not self.hidden:
            surface.blit(self.image, self.rect)
            


class Player1(Player):
    def __init__(self, x, y):     # cor              # controles
        super().__init__(x, y, "assets/shelly.png", {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s})

class Player2(Player):
    def __init__(self, x, y):     # cor              # controles
        super().__init__(x, y, "assets/shelly.png", { "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN})