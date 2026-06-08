import pygame

class Player1:
    def __init__(self, x, y, size = 32):
        self.size = size
        self.color = (0, 0, 255) # deixar a cor azul
        self.rect = pygame.Rect(x, y, size, size) #posicao x, posicao y, largura, altura
        self.speed = 1

    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
    
    def draw(self, surface):
        """Desenha o quadrado na tela"""
        pygame.draw.rect(surface, self.color, self.rect)
        

class Player2():
    def __init__(self, x, y, size = 40):
        self.size = size
        self.color = (255, 0, 0) # deixar a cor vermelha
        self.rect = pygame.Rect(x, y, size, size) #posicao x, posicao y, largura, altura
        self.speed = 1

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def draw(self, surface):
        """Desenha o quadrado na tela"""
        pygame.draw.rect(surface, self.color, self.rect)

