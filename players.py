import pygame

class Player1:

    def __init__(self, x, y, size=24):

        self.size = size
        self.color = (0, 0, 255)

        self.rect = pygame.Rect(x, y, size, size)

        self.speed = 1

        self.hidden = False

    def move(self, mapa):

        old_x = self.rect.x
        old_y = self.rect.y

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_d]:
            self.rect.x += self.speed

        if keys[pygame.K_w]:
            self.rect.y -= self.speed

        if keys[pygame.K_s]:
            self.rect.y += self.speed

        for wall in mapa.walls:
            if self.rect.colliderect(wall):
                self.rect.x = old_x
                self.rect.y = old_y

        for water in mapa.waters:
            if self.rect.colliderect(water):
                self.rect.x = old_x
                self.rect.y = old_y

        self.hidden = False

        for bush in mapa.bushes:
            if self.rect.colliderect(bush):
                self.hidden = True

    def draw(self, surface):

        if not self.hidden:
            pygame.draw.rect(surface, self.color, self.rect)


class Player2:

    def __init__(self, x, y, size=24):

        self.size = size
        self.color = (255, 0, 0)

        self.rect = pygame.Rect(x, y, size, size)

        self.speed = 1

        self.hidden = False

    def move(self, mapa):

        old_x = self.rect.x
        old_y = self.rect.y

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        for wall in mapa.walls:
            if self.rect.colliderect(wall):
                self.rect.x = old_x
                self.rect.y = old_y

        for water in mapa.waters:
            if self.rect.colliderect(water):
                self.rect.x = old_x
                self.rect.y = old_y

        self.hidden = False

        for bush in mapa.bushes:
            if self.rect.colliderect(bush):
                self.hidden = True

    def draw(self, surface):

        if not self.hidden:
            pygame.draw.rect(surface, self.color, self.rect)