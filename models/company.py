class Company:
    def __init__(self, name: str):
        self._name: str = name
        self.ships = []
        self.ccs = []
        self._money: int = 10000000
        self.done_contracts: list = []

    @property
    def name(self):
        return self._name

    def buy_ship(self, ship):
        if ship.price > self._money:
            return False
        self._money -= ship.price
        self.ships.append(ship)
        return True

    def sell_ship(self, ship):
        self._money += ship.value
        self.ships.remove(ship)

    @property
    def get_current_money(self):
        return self._money
