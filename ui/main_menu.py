import pygame
import sys

from ui.screen import Screen
from common.constants import WINDOW_WIDTH, WINDOW_HEIGHT

from common.colors import WHITE, FONT_DARK
from common.helpers import draw_text


class MainMenu(Screen):
    def __init__(self, screen, clock, bg, font, start_button_action):
        super().__init__('loading_screen', screen, clock)
        self.font: pygame.font.Font = font
        self.bg = bg
        self.start_button_action = start_button_action

    def startup_screen(self):
        click = False
        run = True
        comp_name = ""
        while run:
            self.screen.blit(self.bg, (0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(200, 200, 600, 300), 0, 5)

            draw_text("Welcome to PortsOfClasses", FONT_DARK, self.screen, 220, 220, 50)
            draw_text("Created by 4BHEL", FONT_DARK, self.screen, 220, 260, 20)
            draw_text("Insert your Company's name and press Start", FONT_DARK, self.screen, 220, 310, 35)

            name_box = pygame.Rect(220, 350, 400, 60)
            pygame.draw.rect(self.screen, (0, 0, 0), name_box, 0, 5)
            input = self.font.render(comp_name, True, WHITE)
            self.screen.blit(input, input.get_rect(center=name_box.center))

            start_button = pygame.Rect(220, 420, 130, 60)

            mx, my = pygame.mouse.get_pos()
            if start_button.collidepoint((mx, my)):
                if click:
                    self.start_button_action(comp_name)

            pygame.draw.rect(self.screen, (0, 161, 255), start_button, 0, 4)
            draw_text("START", FONT_DARK, self.screen, 230, 435, 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                if event.type == pygame.MOUSEBUTTONUP:
                    click = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_BACKSPACE:
                        comp_name = comp_name[:-1]
                    else:
                        if len(comp_name) < 14:
                            comp_name += event.unicode

            pygame.display.update()
            self.clock.tick(60)
