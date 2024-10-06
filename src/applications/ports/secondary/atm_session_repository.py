from abc import ABC, abstractmethod
from typing import Optional

from src.domains.entities.account import Account
from src.entities.atm_session import ATMSession


class ATMSessionRepository(ABC):
    @abstractmethod
    def create_session(self, card_number: str) -> bool:
        pass

    @abstractmethod
    def get_session(self, card_number: str) -> Optional[ATMSession]:
        pass

    @abstractmethod
    def delete_session(self, card_number: str) -> bool:
        pass

    @abstractmethod
    def select_account(self, card_number: str, account: Account) -> bool:
        pass

    @abstractmethod
    def enter_pin(self, card_number: str, pin: str) -> bool:
        pass

    @abstractmethod
    def eject_card(self, card_number: str) -> bool:
        pass
