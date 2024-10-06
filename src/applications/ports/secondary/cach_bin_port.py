from abc import ABC, abstractmethod


class CashBin(ABC):
    @abstractmethod
    def dispense_cash(self, amount) -> bool:
        pass
