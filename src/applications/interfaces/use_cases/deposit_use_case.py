from abc import abstractmethod


class DepositUseCase:
    @abstractmethod
    def execute(self, card_number: str, amount: int) -> bool:
        pass
