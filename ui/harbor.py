import pygame
from ui.screen import Screen
from models import HarborBase, Company
from typing import List


class HarborScreen(Screen):
    def __init__(self, company: Company, bg, screen: pygame.Surface, clock: pygame.time.Clock, harbors: List[HarborBase]):
        super().__init__("overview_screen", screen, clock)
        self.bg = bg
        self.company = company

        self.overview_action = None

        self.harbors: List[HarborBase] = harbors

    def startup_screen(self):
        run = True
        fields = {}
        click = False
        while run:
            self.screen.blit(self.bg, (0, 0))
            # pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(50, 50, 900, 600), 0, 5)

            mx, my = pygame.mouse.get_pos()
            # print(fields)
            for field in fields:
                if fields[field][1].collidepoint((mx, my)):
                    if click:
                        pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                if event.type == pygame.MOUSEBUTTONUP:
                    click = False

            pygame.display.update()
            self.clock.tick(60)
