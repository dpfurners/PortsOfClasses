import datetime

from models.harbor import HarborBase


class ContractBase:
    def __init__(self, source: HarborBase, dst: HarborBase, total: int, quantity: int, goods: str, time: datetime.time):
        self.source: HarborBase = source
        self.destination: HarborBase = dst
        self.total: int = total
        self.quantity: int = quantity
        self.goods: str = goods
        self.time: datetime.time = time
