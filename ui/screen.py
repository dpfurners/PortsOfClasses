import pygame
import sys

from common.colors import WHITE
from common.helpers import draw_text


class Screen:
    def __init__(self, screen_name, screen, clock):
        self.screen_name = screen_name
        self.screen = screen
        self.clock = clock

    def startup_screen(self):
        run = True
        while run:
            self.screen.fill((0, 0, 0))

            draw_text(self.screen_name, WHITE, self.screen, 20, 20, 30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            pygame.display.update()
            self.clock.tick(60)
