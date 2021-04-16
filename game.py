import threading
from agent import *


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
