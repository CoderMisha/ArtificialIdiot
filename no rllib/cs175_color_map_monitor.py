import pygame
import datetime

pygame.init()

width = 960 // 3
height = 540 // 3
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Color Map Monitor')

font = pygame.font.SysFont(None, 12)
clock = pygame.time.Clock()

running = True


while running:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        try:
            screen.blit(pygame.transform.scale(pygame.image.load('cm_output.png'), (width, height)), (0, 0))
        except FileNotFoundError:
            pass
        else:
            screen.blit(font.render(datetime.datetime.now().strftime('%m/%d %H:%M:%S'), True, (0, 0, 0)), (5, 5))
            pygame.display.update()
        clock.tick(12)

    except KeyboardInterrupt:
        running = False
