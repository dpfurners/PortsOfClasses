from models import Company
from typing import Tuple


class ShipBase:
    def __init__(self, type: str, name: str, price: int, capacity: int):
        self.type: str = type
        self._name: str = name
        self._owner: Company | None = None
        self.value: int | None = None
        self.price: int = price
        self.capacity: int = capacity

        # self.state: int = 100
        # self.damages: list = []
        # self.position: int = ()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, company: Company):
        self._owner = company

    def __repr__(self):
        return f"<ShipBase [{self.type}] name={self._name}>"


class TaxShip(ShipBase):
    tax: int
    tax_time: int
