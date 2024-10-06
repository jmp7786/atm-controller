from abc import abstractmethod


class SelectAccountUseCase:
    @abstractmethod
    def execute(self, card_number: str, account_id: str) -> bool:
        pass
