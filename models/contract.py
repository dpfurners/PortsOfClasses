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
        self.started: datetime.datetime | None = None

    def get_ending(self) -> datetime.datetime:
        if self.started:
            return self.started + datetime.timedelta(seconds=self.time.second)

    def done(self) -> bool:
        if self.started:
            if datetime.datetime.now() > self.get_ending():
                return True
            else:
                return False

    def strfdelta(self) -> str:
        if self.started:
            delta = self.get_ending() - datetime.datetime.now()
            minutes, seconds = divmod(delta.seconds, 60)
            if seconds < 10:
                return f"{minutes}:0{seconds}"
            else:
                return f"{minutes}:{seconds}"
