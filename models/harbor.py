import pygame
from typing import List


class HarborBase:
    def __init__(self, name, description, country, position, capacity, picture):
        self.name: str = name
        self.description: str = description
        self.country: str = country
        self.position: int = position
        self.capacity: int = capacity
        self.picture: pygame.Surface = picture
        self.available_contracts: list = []

    def __repr__(self):
        return f"<HarborBase [{self.country}] {self.name}>"

    def sign_contract(self):
        pass