from abc import ABC, abstractmethod


class BankingService(ABC):
    @abstractmethod
    def validate_pin(self, card_number: str, pin: str):
        pass
