import pygame
import sys

from ui.screen import Screen
from ui.harbor import HarborScreen
from common.helpers import draw_text
from common.colors import FONT_DARK, WHITE

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

    def load_menu(self):
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(15, 485, 150, 200), 0, 2)

        # Display Harbor
        harbor_btn = pygame.Rect(15, 485, 150, 30)
        self.screen.blit(self.anker, (23, 490))
        draw_text("Harbors", FONT_DARK, self.screen, 55, 495, 25)

        # Display Own Ships
        ships_btn = pygame.Rect(15, 515, 150, 30)
        self.screen.blit(self.boat, (20, 520))
        draw_text("Your Ships", FONT_DARK, self.screen, 55, 525, 25)

    def startup_screen(self):
        run = True
        fields = {}
        click = False
        while run:
            self.screen.blit(self.bg, (0, 0))

            self.display_harbors()
            self.load_menu()

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


