from pygame import *
from random import randint, choice
import math

#^ 1. Клас для кулі 
class Circle:
    def __init__(self, x, y, r, col):
        self.x = x
        self.y = y
        self.radius = r
        self.color = col

    def draw(self, screen):
        draw.circle(screen, self.color, (self.x, self.y), self.radius)

#^ 2. Клас для гравця 
class Player(Circle):
    def __init__(self, x, y, r, col, id):
        super().__init__(x, y, r, col)
        self.id = id
        self.speed = 5
    #^ Рух
    def update(self):
        keys = key.get_pressed()

        if keys[K_w]: self.y -= self.speed
        if keys[K_s]: self.y += self.speed
        if keys[K_a]: self.x -= self.speed
        if keys[K_d]: self.x += self.speed
    #^ Перевіка колізій

    #^ Відображення
    def draw(self, screen):
        draw.circle(screen, self.color, (W//2, H//2), self.radius)

food_colors = [
    "#46b050",
    "#b53838",
    "#c7be3d",
    "#39c9d4",
    "#3a30c6"
]
#^ 3. Клас для їжі 
class Food(Circle):
    def __init__(self):
        self.x = randint(-1 * MAP_W // 2, 1 * MAP_W // 2)
        self.y = randint(-1 * MAP_H // 2, 1 * MAP_H // 2)
        self.color = choice(food_colors)
        self.radius = 10
        
    def check_colision(self, player: Player):
        dx = self.x - player.x
        dy = self.y - player.y
        return math.hypot(dx, dy) <= self.radius + player.radius

    #^ Відображення (відносне гравця)
    def draw(self, screen, player):
        draw.circle(screen, self.color, (self.x - player.x + W // 2, self.y - player.y + H // 2), self.radius)


from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 8080))
my_data = list(map(int, sock.recv(64).decode().strip().split(','))) 
#*"*#%&^&$%*@#(&)@#$*@#^$&)" -> '    1,0,0,20   ' -> "1,0,0,20" -> [1,0,0,20]
sock.setblocking(False)

init()

W, H = 1000, 1000
MAP_W, MAP_H = 3000, 3000
screen = display.set_mode((1000, 1000))
clock = time.Clock()
f = font.Font(None, 50)
lose = False

running = True

p = Player(my_data[1], my_data[2], my_data[3], "#427544", my_data[0])

foods = [Food() for _ in range(400) ]


while running:
    for e in event.get():
       if e.type == QUIT:
           running = False


    screen.fill("#d8d7c7")
    #* місце для відображення об'єктів
    p.draw(screen)
    for f in foods:
        f.draw(screen, p)
        if f.check_colision(p):
            p.radius += 1
            foods.remove(f)


    #* місце для апдейту об'єктів
    p.update()

    display.update()
    clock.tick(60)

quit()