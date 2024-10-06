from src.applications.ports.secondary.cach_bin_port import CashBin


class CashBinImpl(CashBin):
    def __init__(self, total_cash):
        self.total_cash = total_cash

    def dispense_cash(self, amount) -> bool:
        if self.total_cash >= amount:
            self.total_cash -= amount
            return True
        else:
            return False
