from abc import abstractmethod


class EnterPinUseCase:
    @abstractmethod
    def execute(self, car_number: str, pin: str) -> bool:
        pass
