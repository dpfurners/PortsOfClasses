import pygame
import sys
import random
from math import floor

from typing import List

from ui.screen import Screen
from models import Company, ShipBase, ContractBase
from common.helpers import draw_text
from common.colors import FONT_DARK, WHITE
from common.constants import SHIP_NAMES


class ContractScreen(Screen):
    def __init__(self, company: Company, bg, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__("ship_screen", screen, clock)
        self.bg = bg
        self.company = company
        self.back_action = None
        self.contract = None

    def display_contract(self, contract: ContractBase):
        self.contract = contract
        self.startup_screen()

    def startup_screen(self):
        click = False
        while 1:
            self.screen.blit(self.bg, (0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(50, 50, 900, 600), 0, 5)

            draw_text("Contract", FONT_DARK, self.screen, 75, 75, 50)
            draw_text(f"Balance: {self.company.get_current_money:_}$", FONT_DARK, self.screen, 500, 75, 25)
            draw_text(f"Max. Capacity: {max([ship.capacity for ship in self.company.ships if ship.contract is None]):_}", FONT_DARK, self.screen, 500, 100, 25)
            self.fields = {}

            go_on = pygame.Rect(864, 65, 50, 50)
            self.screen.blit(pygame.image.load("./resources/textures/cross.png"), (864, 65))
            # pygame.draw.rect(self.screen, (255, 161, 0), go_on, 0, 2)
            self.fields["go_on"] = [0, go_on]

            mx, my = pygame.mouse.get_pos()
            for field in self.fields:
                if self.fields[field][1].collidepoint((mx, my)):
                    if click:
                        if field == "go_on":
                            self.back_action()

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
