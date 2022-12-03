import pygame
from math import floor
from ui.screen import Screen
from models import HarborBase, Company, ShipBase, ContractBase
from common.constants import HARBORS_PER_PAGE
from typing import List
from common.helpers import draw_text, new_button
from common.colors import FONT_DARK, WHITE


class HarborScreen(Screen):
    def __init__(self, company: Company, bg, screen: pygame.Surface, clock: pygame.time.Clock, harbors: List[HarborBase]):
        super().__init__("overview_screen", screen, clock)
        self.bg = bg
        self.company = company

        self.overview_action = None
        self.contract_action = None

        self.harbors: List[HarborBase] = harbors

        self.inspect: HarborBase | None = None

        self.current_page = 0

        self.pages: List[List[HarborBase]] = list(self.get_pages())

        self.fields = {}

    def get_pages(self):
        for i in range(0, len(self.harbors), HARBORS_PER_PAGE):
            yield self.harbors[i:i+HARBORS_PER_PAGE]

    def display_available_harbors(self):
        for index, harbor in enumerate(self.pages[self.current_page]):
            x = y = 0
            x = 75
            y = 55 * (floor(index)) + 125
            rect = pygame.Rect(x, y, 420, 50)
            if self.inspect == harbor:
                pygame.draw.rect(self.screen, (255, 161, 0), rect, 0, 2)
            else:
                pygame.draw.rect(self.screen, (0, 161, 255), rect, 0, 2)
            draw_text(harbor.name, FONT_DARK, self.screen, x + 5, y + 5, 35)  # Display Harbor Name
            draw_text(harbor.country, FONT_DARK, self.screen, x + 5, y + 30, 20)  # Display Harbor Country
            draw_text(f"Contracts: {len(harbor.available_contracts)}", FONT_DARK, self.screen, x + 205, y + 30, 20)

            # draw_text(f"Contracts: {len(harbor.available_contracts)}", FONT_DARK, self.screen, x + 5, y + 50, 30)
            self.fields[harbor] = [harbor, rect]

    def display_contracts(self):
        for index, contract in enumerate(self.inspect.available_contracts):
            x = y = 0
            x = 500
            y = 55 * (floor(index)) + 125
            rect = new_button(self.screen, (x, y), (420, 50), color=(0, 161, 255))
            draw_text(contract.destination.name, FONT_DARK, self.screen, x + 5, y + 5, 35)  # Display Harbor Name
            draw_text(f"Quantity: {contract.quantity:_}", FONT_DARK, self.screen, x + 5, y + 30, 20)  # Display Harbor Country
            draw_text(f"Pricing: {contract.total:_}$", FONT_DARK, self.screen, x + 205, y + 30, 20)
            draw_text(contract.time.strftime('%M:%S'), FONT_DARK, self.screen, x + 350, y + 15, 30)

            # draw_text(f"Contracts: {len(harbor.available_contracts)}", FONT_DARK, self.screen, x + 5, y + 50, 30)
            self.fields[contract] = [contract, rect]

    def startup_screen(self):
        run = True
        click = False
        if self.inspect is None:
            self.inspect = self.pages[0][0]
        while run:
            self.fields = {}
            self.screen.blit(self.bg, (0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(50, 50, 900, 600), 0, 5)

            draw_text("Harbors", FONT_DARK, self.screen, 75, 75, 50)
            draw_text(f"Balance: {self.company.get_current_money:_}$", FONT_DARK, self.screen, 500, 75, 25)
            try:
                draw_text(f"Max. Capacity: {max([ship.capacity for ship in self.company.ships if ship.contract is None]):_}", FONT_DARK, self.screen, 500, 100, 25)
            except ValueError:
                draw_text(f"Max. Capacity: 0", FONT_DARK, self.screen, 500, 100, 25)
            self.display_available_harbors()
            self.display_contracts()

            go_on = new_button(self.screen, (864, 65), (50, 50), picture="./resources/textures/cross.png")
            self.fields["go_on"] = [0, go_on]

            mx, my = pygame.mouse.get_pos()
            # print(fields)
            for field in self.fields:
                if self.fields[field][1].collidepoint((mx, my)):
                    if click:
                        if isinstance(field, HarborBase):
                            self.inspect = self.fields[field][0]
                            pygame.time.wait(100)
                        elif isinstance(field, ContractBase):
                            self.contract_action(field)
                        else:
                            if field == "back":
                                self.inspect = None
                                pygame.time.wait(100)
                            elif field == "go_on":
                                self.overview_action()

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
