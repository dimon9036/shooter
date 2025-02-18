import pygame
from random import randint
pygame.init() 

points = 0
FPS = 60
lost_points = 0

font_stat = pygame.font.SysFont("Arial", 30)
points_lb = font_stat.render(f"Вбито: {points}", True, (255, 255, 255))

lost_lb = font_stat.render(f"Пропущено: {lost_points}", True, (255, 255, 255))

win_width, win_height = 700, 500

window = pygame.display.set_mode((win_width, win_height))

timer = pygame.time.Clock()

background = pygame.image.load("galaxy.jpg")
background = pygame.transform.scale(background, (win_width, win_height))

pygame.display.set_caption("Шутер")

pygame.mixer.music.load("space.ogg")


pygame.mixer.music.load("deadmau5 - Familiars (From the Game _World of Tanks Blitz_) [4K Visualizer].mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

fire_sound = pygame.mixer.Sound("fire.ogg")

background1 = pygame.image.load("galaxy2.jpg")
background1 = pygame.transform.scale(background1, (win_width, win_height))
try:
    with open("record.txt", "r", encoding="Utf-8") as file:
        record = int(file.read())
except:
    record = 0

class Sprite:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
    def move(self, a, d):
        keys = pygame.key.get_pressed()
        if keys[a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[d]:
            if self.rect.right < win_width:
                self.rect.x += self.speed

    def fire(self):
        bullets.append(Bullet(self.rect.centerx -13, self.rect.y, 25, 50, bullet_image, 15))
        fire_sound.play()



class Enemy(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
    def move(self):
        global lost_points, lost_lb
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.x = randint(0, win_width - 50)
            self.rect.y = randint(-800, -50)
            lost_points +=1
            lost_lb = font_stat.render(f"Пропущено: {lost_points}", True, (255, 255, 255))

class Bullet(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed 

    def move(self):
        self.rect.y -= self.speed
        if bullet.rect.y <= 0:
            bullets.remove(self)


player1 = Player(0, 400, 50, 50, pygame.image.load("rocket.png"), 5)

enemies = []
enemy_image = pygame.image.load("asteroid.png")

bullets = []
bullet_image = pygame.image.load("bullet.png")

for i in range(5):
    enemies.append(Enemy(randint(0, win_width - 50), randint(-800, -50), 50, 50, enemy_image, 2))



font = pygame.font.SysFont("Arial", 70)
lose = font.render("You lose!", True, (255, 0, 0))
win = font.render("You won!", True, (0, 255, 0))

button_image = pygame.image.load("button.png")
button = Sprite(250, 300, 200, 150, button_image)

def new_record(record, points):
    if record < points:
        with open("record.txt", "w", encoding="Utf-8") as file:
            file.write(str(points))
        window.blit(font_stat.render(f"Новий рекорд: {points}", True, (255, 255, 0)), (200, 0))
 


game = True
finish = False
menu = True

while game:
    if menu:
        window.blit(background1, (0, 0))
        button.draw()

    if not finish and not menu:
        window.blit(background, (0, 0))
        window.blit(points_lb, (0, 0))      
        window.blit(lost_lb, (0, 40))

        for enemy in enemies:
            enemy.draw()
            enemy.move()
            if enemy.rect.colliderect(player1.rect):
                finish = True
                window.blit(lose, (200, 0))
                new_record(record, points)
            for bullet in bullets:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.rect.x = randint(0, win_width - 50)
                    enemy.rect.y = randint(-800, -50)   
                    bullets.remove(bullet)
                    points += 1
                    points_lb = font_stat.render(f"Вбито: {points}", True, (255, 255, 255)) 
        player1.draw()
        player1.move(pygame.K_a, pygame.K_d)

        if lost_points >= 5:
            finish = True
            window.blit(lose, (200, 0)) 
            new_record(record, points)


        for bullet in bullets:
            bullet.draw()
            bullet.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player1.fire()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and finish == True:
            finish = False       
            player1 = Player(0, 400, 50, 50, pygame.image.load("rocket.png"), 5)
            points = 0
            lost_points = 0
            bullets.clear()
            enemies.clear()
            for i in range(5):
                enemies.append(Enemy(randint(0, win_width - 50), randint(-800, -50), 50, 50, enemy_image, 2))
            points_lb = font_stat.render(f"Вбито: {points}", True, (255, 255, 255))
            lost_lb = font_stat.render(f"Пропущено: {lost_points}", True, (255, 255, 255))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if button.rect.collidepoint(x, y):
                menu = False
                pygame.mixer.music.load("space.ogg")
                pygame.mixer.music.load("space.ogg")
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)

    pygame.display.update()
    timer.tick(FPS)

pygame.time.delay(30)