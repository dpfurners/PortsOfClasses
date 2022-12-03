import pygame
import sys

from ui.screen import Screen
from ui.harbor import HarborScreen

from models import Company


class OverviewScreen(Screen):
    def __init__(self, company: Company, screen: pygame.Surface, clock: pygame.time.Clock, ship_shop: callable):
        super().__init__("overview_screen", screen, clock)
        self.bg = pygame.image.load("./resources/textures/map.jpg")
        self.company = company

        self.ship_shop_action = ship_shop
        self.harbor_overview: HarborScreen | None = None

        self.anker = pygame.image.load("./resources/textures/pins/anker.png")
        self.boat = pygame.image.load("./resources/textures/pins/boat_pin.png")

    def display_harbors(self):
        for harbor in self.harbor_overview.harbors:
            self.screen.blit(self.anker, harbor.position)

    def startup_screen(self):
        run = True
        fields = {}
        click = False
        while run:
            self.screen.blit(self.bg, (0, 0))
            # pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(50, 50, 900, 600), 0, 5)

            self.display_harbors()

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


