from src.applications.interfaces.use_cases.eject_card_use_case import \
    EjectCardUseCase
from src.applications.ports.secondary.atm_session_repository import \
    ATMSessionRepository


class EjectCardUseCaseImpl(EjectCardUseCase):
    def __init__(self, atm_session_repository: ATMSessionRepository):
        self.atm_session_repository = atm_session_repository

    def execute(self, card_number: str) -> bool:
        return self.atm_session_repository.eject_card(card_number)
