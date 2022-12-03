import pygame
import sys

from ui.screen import Screen
from ui.harbor import HarborScreen
from common.helpers import draw_text
from common.colors import FONT_DARK, WHITE
from common.constants import OVERVIEW_MENU_X, OVERVIEW_MENU_Y

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
        self.contract = pygame.image.load("./resources/textures/contracts.png")

    def display_harbors(self):
        for harbor in self.harbor_overview.harbors:
            self.screen.blit(self.anker, harbor.position)

    def load_menu(self):
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(OVERVIEW_MENU_X, OVERVIEW_MENU_Y, 150, 100), 0, 2)
        draw_text("Your:", FONT_DARK, self.screen, OVERVIEW_MENU_X + 5, OVERVIEW_MENU_Y + 5, 30)
        # Display Contracts
        contracts_btn = pygame.Rect(OVERVIEW_MENU_X, OVERVIEW_MENU_Y + 23, 150, 33)
        self.screen.blit(self.contract, (OVERVIEW_MENU_X + 8, OVERVIEW_MENU_Y + 30))
        draw_text("Contracts", FONT_DARK, self.screen, OVERVIEW_MENU_X + 40, OVERVIEW_MENU_Y + 35, 25)

        # Display Own Ships
        own_ships_btn = pygame.Rect(OVERVIEW_MENU_X, OVERVIEW_MENU_Y + 57, 150, 35)
        self.screen.blit(self.boat, (OVERVIEW_MENU_X + 5, OVERVIEW_MENU_Y + 60))
        draw_text("Ships", FONT_DARK, self.screen, OVERVIEW_MENU_X + 40, OVERVIEW_MENU_Y + 65, 25)

        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(OVERVIEW_MENU_X, OVERVIEW_MENU_Y + 105, 150, 100), 0, 2)
        draw_text("Available:", FONT_DARK, self.screen, OVERVIEW_MENU_X + 5, OVERVIEW_MENU_Y + 110, 30)

        # Display Harbors
        harbor_btn = pygame.Rect(OVERVIEW_MENU_X, OVERVIEW_MENU_Y + 128, 150, 35)
        self.screen.blit(self.anker, (OVERVIEW_MENU_X + 8, OVERVIEW_MENU_Y + 135))
        draw_text("Harbors", FONT_DARK, self.screen, OVERVIEW_MENU_X + 40, OVERVIEW_MENU_Y + 140, 25)

        # Display Ship Shop
        ships_shops_btn = pygame.Rect(OVERVIEW_MENU_X, OVERVIEW_MENU_Y + 164, 150, 35)
        self.screen.blit(self.boat, (OVERVIEW_MENU_X + 5, OVERVIEW_MENU_Y + 167))
        draw_text("Ships", FONT_DARK, self.screen, OVERVIEW_MENU_X + 40, OVERVIEW_MENU_Y + 172, 25)

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


