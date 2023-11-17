import numpy as np
import math
from random import choice
import random

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
TANK_COLOR = 0x008000
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

score = 0

class Ball:
    def __init__(self, screen: pygame.Surface, x, y = 520):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = random.randint(5, 15)
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        new_x = self.x + self.vx
        new_y = self.y - self.vy
        
        if 5 + self.r < new_x < 796 - self.r:
            self.x = new_x
        else:
            self.vx = - int(self.vx * 0.6)
            self.vy = np.sign(self.vy) * (abs(self.vy)*0.8)
        if new_y < 596 - self.r:
            self.y = new_y
        else:
            self.vy = - int(self.vy * 0.6)
            self.vx = np.sign(self.vx) * (abs(self.vx)*0.4)
            
        self.vy -= 2

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5 <= self.r + obj.r:
            return True
        else:
            return False
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

class Gun_1:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 100

    def move(self, motion):
        if 50 <= self.x:
            self.x += motion
        else:
            if motion > 0:
                self.x += motion

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if (event.pos[0]-self.x) > 0:
                self.an = math.atan((event.pos[1]-520) / (event.pos[0]-self.x))
            elif (event.pos[0]-self.x) < 0:
                self.an = math.atan((event.pos[1]-520) / (event.pos[0]-self.x)) + math.pi
            else:
                self.an = (- 1) ** ((event.pos[1]-520) >= 0) * math.pi / 2
            
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        "Координаты орудия:"
        x = self.x
        y = 520
        h = 5
        L = 20 + int(self.f2_power / 4 * 3)
        
        if (self.an != math.pi / 2) and (self.an != - math.pi / 2):
            x1 = x - h * (math.sin(-self.an) + math.cos(-self.an))
            y1 = y + h * (math.sin(-self.an) - math.cos(-self.an))
            x2 = x1 + L * math.cos(-self.an)
            y2 = y1 - L * math.sin(-self.an)
            x3 = x1 + 2 * h * math.sin(-self.an)
            y3 = y1 + 2 * h * math.cos(-self.an)
            x4 = x3 + L * math.cos(-self.an)
            y4 = y3 - L * math.sin(-self.an)
        else:
            if self.an > 0:
                k = 1
            else:
                k = - 1
            x1 = x - h
            y1 = y + k * h
            x2 = x1
            y2 = y1 - k * L
            x3 = x + h
            y3 = y1
            x4 = x3
            y4 = y3 - k * L

        pygame.draw.lines(self.screen, BLACK, True,
                  [[x - 38, y + 4], [x - 38, y - 10]], 2)
        pygame.draw.polygon(self.screen, BLUE, 
                     [[x - 38, y], [x - 47, y - 5], 
                      [x - 38, y - 10]])
        
        pygame.draw.polygon(self.screen, self.color, 
                     [[x1, y1], [x2, y2], 
                      [x4, y4], [x3, y3]])
        pygame.draw.circle(
            screen,
            TANK_COLOR,
            (x, y + 5),
            15
        )
        pygame.draw.polygon(self.screen, TANK_COLOR, 
                     [[x - 50, y + 25], [x - 40, y + 5], 
                      [x + 40, y + 5], [x + 50, y + 25]])
        pygame.draw.lines(self.screen, BLACK, True,
                  [[x - 50, y + 25], [x - 40, y + 40], [x + 40, y + 40], [x + 50, y + 25]], 3)
        for i in range(6):
            pygame.draw.circle(
            screen,
            BLACK,
            (x - 35 + i * 14.2, y + 32),
            8
        )
        
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 2
            self.color = RED
        else:
            self.color = GREY

class Gun_2:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 700

    def move(self, motion): 
        self.x += motion

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if (event.pos[0]-self.x) > 0:
                self.an = math.atan((event.pos[1]-520) / (event.pos[0]-self.x))
            elif (event.pos[0]-self.x) < 0:
                self.an = math.atan((event.pos[1]-520) / (event.pos[0]-self.x)) + math.pi
            else:
                self.an = (- 1) ** ((event.pos[1]-520) >= 0) * math.pi / 2
            
            #self.an = math.atan((event.pos[1]-450) / (event.pos[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        "Координаты орудия:"
        x = self.x
        y = 520
        h = 5
        L = 20 + int(self.f2_power / 4 * 3)
        
        if (self.an != math.pi / 2) and (self.an != - math.pi / 2):
            x1 = x - h * (math.sin(-self.an) + math.cos(-self.an))
            y1 = y + h * (math.sin(-self.an) - math.cos(-self.an))
            x2 = x1 + L * math.cos(-self.an)
            y2 = y1 - L * math.sin(-self.an)
            x3 = x1 + 2 * h * math.sin(-self.an)
            y3 = y1 + 2 * h * math.cos(-self.an)
            x4 = x3 + L * math.cos(-self.an)
            y4 = y3 - L * math.sin(-self.an)
        else:
            if self.an > 0:
                k = 1
            else:
                k = - 1
            x1 = x - h
            y1 = y + k * h
            x2 = x1
            y2 = y1 - k * L
            x3 = x + h
            y3 = y1
            x4 = x3
            y4 = y3 - k * L

        pygame.draw.lines(self.screen, BLACK, True,
                  [[x + 38, y + 4], [x + 38, y - 10]], 2)
        pygame.draw.polygon(self.screen, RED, 
                     [[x + 38, y], [x + 47, y - 5], 
                      [x + 38, y - 10]])
        
        pygame.draw.polygon(self.screen, self.color, 
                     [[x1, y1], [x2, y2], 
                      [x4, y4], [x3, y3]])
        pygame.draw.circle(
            screen,
            TANK_COLOR,
            (x, y + 5),
            15
        )
        pygame.draw.polygon(self.screen, TANK_COLOR, 
                     [[x - 50, y + 25], [x - 40, y + 5], 
                      [x + 40, y + 5], [x + 50, y + 25]])
        pygame.draw.lines(self.screen, BLACK, True,
                  [[x - 50, y + 25], [x - 40, y + 40], [x + 40, y + 40], [x + 50, y + 25]], 3)
        for i in range(6):
            pygame.draw.circle(
            screen,
            BLACK,
            (x - 35 + i * 14.2, y + 32),
            8
        )
        
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 2
            self.color = RED
        else:
            self.color = GREY

class Target_0:
    def __init__(self, screen):
        self.points = 0
        self.live = 1
        self.screen = screen
        self.x = random.randint(100 - 50, 120 + 50)
        self.y = random.randint(100, 300)
        self.r = 15
        self.color = RED
        
        self.vx = 0 
        self.vy = 0

    def move(self):
        """Сброс бомбочек"""

        new_x = self.x + self.vx
        new_y = self.y - self.vy
        
        if 15 < new_x < 786:
            self.x = new_x
        else:
            self.vx = - int(self.vx * 0.6)
            self.vy = np.sign(self.vy) * (abs(self.vy) * 0.9)
        if new_y < 546:
            self.y = new_y
        else:
            self.vy = - int(self.vy * 0.9)
            self.vx = np.sign(self.vx) * (abs(self.vx) * 0.4)
            
        self.vy -= 0.5

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = (100 - 50, 100 + 50)
        self.y = random.randint(100, 300)
        self.r = 15
        self.color = RED
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            screen,
            BLACK,
            (self.x, self.y),
            self.r + 2, 4
        )
        pygame.draw.circle(
            screen,
            choice([RED, YELLOW]),
            (self.x, self.y),
            self.r - 5
        )
        pygame.draw.line(screen, BLACK, [self.x - self.r, self.y], [self.x + self.r, self.y], 4)
        pygame.draw.line(screen, BLACK, [self.x, self.y - self.r], [self.x, self.y + self.r], 4)

class Target_1:
    def __init__(self, screen):
        self.points = 0
        self.live = 1
        self.screen = screen
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 400)
        self.r = random.randint(40, 60)
        self.color = RED

        self.vx = random.randint(- 4, 4) 
        self.vy = random.randint(- 4, 4)

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = random.randint(100, 700)
        self.y = random.randint(50, 530)
        self.r = random.randint(20, 50)
        self.color = choice(GAME_COLORS)
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def move(self):
         """Движение мишени 1."""
         if abs(self.vx) <= 10 and abs(self.vy) <= 30:
             self.vx += random.randint(- 10, 10)
             self.vy += random.randint(- 10, 10)
         else:
             self.vx = np.sign(self.vx) * (abs(self.vx)*0.5)
             self.vy = np.sign(self.vy) * (abs(self.vy)*0.5)

         new_x = self.x + self.vx
         new_y = self.y - self.vy
        
         if 100 < new_x < 700:
             self.x = new_x
         else:
             self.vx = - self.vx
         if 100 < new_y < 500:
             self.y = new_y
         else:
             self.vy = - self.vy

    def draw(self):
        x = self.x 
        y = self.y 
        r = self.r
        pygame.draw.polygon(self.screen, self.color, 
                     [[x + random.randint(- 20, 20), y + random.randint(- 20, 20)], [x + random.randint(- 20, 20), y + r + random.randint(- 20, 20)], 
                      [x + r + random.randint(- 20, 20), y + r + random.randint(- 20, 20)], [x + r + random.randint(- 20, 20), y + random.randint(- 20, 20)]])

class Target_2:
    def __init__(self, screen):
        self.points = 0
        self.live = 1
        self.screen = screen
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 400)
        self.r = random.randint(20, 50)
        self.color = RED
        
        self.vx = random.randint(- 4, 4) 
        self.vy = random.randint(- 4, 4) 

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = random.randint(100, 700)
        self.y = random.randint(50, 530)
        self.r = random.randint(20, 50)
        self.color = RED
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def move(self):
         """Движение мишени 2."""
         if abs(self.vx) <= 10 and abs(self.vy) <= 10:
             self.vx += random.randint(- 4, 4)
             self.vy += random.randint(- 4, 4)
         else:
             self.vx = np.sign(self.vx) * (abs(self.vx)*0.5)
             self.vy = np.sign(self.vy) * (abs(self.vy)*0.5)

         new_x = self.x + self.vx
         new_y = self.y - self.vy
        
         if 100 < new_x < 700:
             self.x = new_x
         else:
             self.vx = - self.vx
         if 100 < new_y < 500:
             self.y = new_y
         else:
             self.vy = - self.vy
        
    def draw(self):
        x_ = self.x
        y_ = self.y
        r_ = self.r + random.randint(0, 10)
        
        pygame.draw.circle(
            screen,
            self.color,
            (x_, y_),
            r_
        )
        pygame.draw.circle(
            screen,
            BLACK,
            (x_, y_),
            r_ + 2, 4
        )
        pygame.draw.circle(
            screen,
            choice(GAME_COLORS),
            (x_, y_),
            r_ - 10
        )
        pygame.draw.line(screen, BLACK, [x_ - r_, y_], [x_ + r_, y_], 4)
        pygame.draw.line(screen, BLACK, [x_, y_ - r_], [x_, y_ + r_], 4)

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
motion_1 = 0
motion_2 = 0

clock = pygame.time.Clock()

gun_1 = Gun_1(screen)
gun_2 = Gun_2(screen)
gun = [gun_1, gun_2]

target_1 = Target_1(screen)
target_2 = Target_2(screen)
target_0 = Target_0(screen)

target = [target_1, target_2, target_0]
finished = False

show = 0
type_bam = 0

while not finished:
    screen.fill(WHITE)
    if show > 0:
        screen.blit(pygame.font.SysFont('Verdana', 30).render('Раунд закончен, целей поражено: ' + str(score), False, (0, 0, 0)), (100, 200))
        if type_bam == 2:
            for i in range(2):
                pygame.draw.circle(
                    screen,
                    RED,
                    (gun[i].x, 520),
                    40
                )
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (gun[i].x, 520),
                    20
                )
        elif type_bam == 1:
            pygame.draw.circle(
                    screen,
                    RED,
                    (gun[0].x, 520),
                    40
                )
            pygame.draw.circle(
                    screen,
                    YELLOW,
                    (gun[0].x, 520),
                    20
                )
        show -= 1
        if show == 0:
            score = 0
        
    gun[0].draw()
    gun[1].draw()
    target[0].draw()
    target[1].draw()
    if show == 0:
        target[2].draw()
    screen.blit(pygame.font.SysFont('Verdana', 40).render(str(score), False, (0, 0, 0)), (30, 20))
    screen.blit(pygame.font.SysFont('Verdana', 20).render('Использовано шаров: ' + str(len(balls)), False, (0, 0, 0)), (200, 40))
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    pygame.key.set_repeat(True)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun[0].fire2_start(event)
            gun[1].fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun[0].fire2_end(event)
            gun[1].fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun[0].targetting(event)
            gun[1].targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                motion_1 = - 0.4
            elif event.key == pygame.K_RIGHT:
                motion_1 = + 0.4
                
            gun[0].move(motion_1)
        if motion_1 == 0:
            motion_2 = - 1
            gun[1].move(motion_2)
        motion_1 = 0

    target[0].move()
    target[1].move()
    if show == 0:
        target[2].move()
    for b in balls:
        b.move()
        if b.hittest(target[0]) and target[0].live:
            target[0].live = 0
            target[0].hit()
            target[0].new_target()

            balls = []
            score += 1

        if b.hittest(target[1]) and target[1].live:
            target[1].live = 0
            target[1].hit()
            target[1].new_target()
            
            balls = []
            score += 1
                
    gun[0].power_up()
    gun[1].power_up()

    if target[2].y > 480 and (target[2].x - gun[0].x) ** 2 < 60 ** 2:
        show = 60
        type_bam = 1
        
        gun_1 = Gun_1(screen)
        gun_2 = Gun_2(screen)
        gun = [gun_1, gun_2]

        target_1 = Target_1(screen)
        target_2 = Target_2(screen)
        target_0 = Target_0(screen)

        target = [target_1, target_2, target_0]

    if gun[0].x + 50 >= gun[1].x - 50:
        show = 60
        type_bam = 2

        gun_1 = Gun_1(screen)
        gun_2 = Gun_2(screen)
        gun = [gun_1, gun_2]

        target_1 = Target_1(screen)
        target_2 = Target_2(screen)
        target_0 = Target_0(screen)

        target = [target_1, target_2, target_0]

pygame.quit()
