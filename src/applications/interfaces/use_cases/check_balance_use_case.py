from abc import abstractmethod


class CheckBalanceUseCase:
    @abstractmethod
    def execute(self, card_number: str) -> int:
        pass
