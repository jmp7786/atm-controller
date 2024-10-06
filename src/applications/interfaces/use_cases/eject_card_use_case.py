from abc import abstractmethod


class EjectCardUseCase:
    @abstractmethod
    def execute(self, card_number: str) -> bool:
        pass
