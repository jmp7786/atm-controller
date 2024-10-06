from abc import abstractmethod


class WithdrawUseCase:
    @abstractmethod
    def execute(self, card_number: str, amount: int) -> bool:
        pass
