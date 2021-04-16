import pygame
import random
import threading
from my_constants import *

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Agent:
    def __init__(self, dots):
        self.dots = dots
        self.x, self.y = self.start_point()
        self.goal = self.goal_point()

    def start(self):
        while self.y < self.goal[1]:
            next_move = self.check_the_front(self.x, self.y)
            sides = self.check_the_sides(self.x, self.y)

            pygame.draw.line(surface, WHITE, (self.x, self.y), (self.x, self.y), width=1)
            pygame.display.flip()
            pygame.time.wait(100)

            if len(next_move) > 0:
                if random.randint(0, 1):
                    self.x += next_move[random.randint(0, len(next_move) - 1)]
                    self.y += 1
                else:
                    if self.x < self.goal[0]:
                        self.x += max(next_move)
                        self.y += 1

                    elif self.x > self.goal[0]:
                        self.x += min(next_move)
                        self.y += 1

                    else:
                        self.x += int(len(next_move) / 2)
                        self.y += 1

            elif len(sides) > 0:
                self.x += sides[random.randint(0, len(sides) - 1)]

            else:
                print('Stuck at', 'x:', self.x, 'y:', self.y)
                return

    def start_point(self):
        while True:
            x, y = random.randint(2, WIDTH - 2), 10
            if len(self.check_the_front(x, y)) != 0:
                return x, y

    def goal_point(self):
        return [random.randint(2, WIDTH - 2), HEIGHT - 10]

    def check_the_front(self, x, y):
        for i in [-2, -1, 0, 1, 2]:
            if (x + i, y + 1) in self.dots:
                return []

        my_list = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (x + i + j, y + 2) in self.dots:
                    break
            else:
                if not abs(i) == 2:
                    my_list.append(i)

        return my_list

    def check_the_sides(self, x, y):
        my_list = []

        for i in [-1, 1]:
            for j in [-1, 0, 1]:
                if i + 1:
                    if (x + 2, y + j) in self.dots:
                        break
                else:
                    if (x - 2, y + j) in self.dots:
                        break
            else:
                my_list.append(i)

        return my_list


def get_random_coordinate():
    x = random.randint(2, WIDTH)
    y = random.randint(20, HEIGHT - 20)
    return x, y


is_running = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not is_running:
                is_running = True
                points = []
                surface.fill((0, 0, 0))
                number_0f_points_on_screen = 4000
                for _ in range(0, number_0f_points_on_screen):
                    coordinate = get_random_coordinate()
                    pygame.draw.circle(surface, RED, coordinate, 1)
                    points.append(coordinate)

                agent = Agent(points)
                pygame.display.flip()
                agent_thread = threading.Thread(target= agent.start, daemon= True)
                agent_thread.start()

            elif not agent_thread.is_alive():
                is_running = False
