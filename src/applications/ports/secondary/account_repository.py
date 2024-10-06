from abc import ABC, abstractmethod
from typing import Optional

from src.domains.entities.account import Account


class AccountRepository(ABC):
    @abstractmethod
    def get_account(self, catd_number: str, account_id: str) -> Optional[Account]:
        pass

    @abstractmethod
    def get_accounts(self, card_id: str) -> Optional[dict[str, Account]]:
        pass

    @abstractmethod
    def save(self, card_number: str, account: Account) -> bool:
        pass
