from abc import abstractmethod
from typing import List

from src.domains.entities.account import Account


class GetAccountsUseCase:
    @abstractmethod
    def execute(self, car_number: str) -> List[Account]:
        pass
