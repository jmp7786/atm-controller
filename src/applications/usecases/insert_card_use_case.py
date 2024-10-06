from src.applications.interfaces.use_cases.insert_card_use_case import \
    InsertCardUseCase
from src.applications.ports.secondary.atm_session_repository import \
    ATMSessionRepository


class InsertCardUseCaseImpl(InsertCardUseCase):
    def __init__(self, atm_session_repository: ATMSessionRepository):
        self.atm_session_repository = atm_session_repository

    def execute(self, card_number: str) -> bool:
        return self.atm_session_repository.create_session(card_number)
