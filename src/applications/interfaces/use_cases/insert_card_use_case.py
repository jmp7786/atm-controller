from abc import abstractmethod

from src.applications.ports.secondary.atm_session_repository import \
    ATMSessionRepository


class InsertCardUseCase:
    @abstractmethod
    def __init__(self, atm_session_repository: ATMSessionRepository):
        self.atm_session_repository = atm_session_repository

    @abstractmethod
    def execute(self, card_number: str) -> bool:
        pass
