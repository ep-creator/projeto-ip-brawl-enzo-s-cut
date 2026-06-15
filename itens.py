import pygame
import math  #precisa pra poder calcular pra onde a bala vai 
class Itens:
    def __init__(self, x, y, radius=5, color=(255, 0, 0)):
        self.posicao = (x, y)
        self.radius = radius
        self.color = color
        
    def draw(self, surface):
        """Desenha o circulo na tela"""
        pygame.draw.circle(surface, center=self.posicao, radius = self.radius, color=self.color)

class Projectile():
    def __init__(self,x , y, target_x, target_y, radius = 6, color= (0,0,0), vel = 10):
        self.x = x
        self.y = y
        self.radius = radius 
        self.color = color
        
        dx = target_x - x
        dy = target_y - y

        distancia = math.hypot(dx, dy) #calcula a distancia por meio da hipotenusa, usa a biblioteca "math"

        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius *2, self.radius *2)
        #cria uma hitbox em volta da bala pra fazer a colisão
        if distancia == 0:
            distancia = 1 #evita a divisao por zero se eles estiverem um em cima do outro  
        
        self.vel_x = (dx / distancia) * vel
        self.vel_y = (dy / distancia) * vel #define a vel da bala 

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y #move a bala 

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y) # faz a hitbox da bala andar

    def draw(self, window):#desenho da bala 
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)

   
       

class Item:
    def __init__(self, x, y, item_type):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.type = item_type  # "life", "damage", "speed"

        if item_type == "life":
            self.color = (0, 255, 0)
        elif item_type == "damage":
            self.color = (255, 0, 0)
        elif item_type == "speed":
            self.color = (0, 0, 255)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
