from abc import ABC, abstractmethod
from typing import List

from src.domains.entities.account import Account


class ATMService(ABC):
    @abstractmethod
    def insert_card(self, card_number: str) -> bool:
        pass

    @abstractmethod
    def enter_pin(self, card_number: str, pin: str) -> bool:
        pass

    @abstractmethod
    def get_accounts(self, card_number: str) -> List[Account]:
        pass

    @abstractmethod
    def select_account(self, card_number: str, account_id: str):
        pass

    @abstractmethod
    def check_balance(self, card_number: str) -> int:
        pass

    @abstractmethod
    def deposit(self, card_number: str, amount: int) -> bool:
        pass

    @abstractmethod
    def withdraw(self, card_number: str, amount: int) -> bool:
        pass

    @abstractmethod
    def eject_card(self, card_number: str) -> bool:
        pass
