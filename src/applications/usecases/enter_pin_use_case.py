from src.applications.interfaces.use_cases.enter_pin_use_case import \
    EnterPinUseCase
from src.applications.ports.secondary.atm_session_repository import \
    ATMSessionRepository
from src.applications.ports.secondary.banking_service_port import \
    BankingService


class EnterPinUseCaseImpl(EnterPinUseCase):
    def __init__(
        self,
        atm_session_repository: ATMSessionRepository,
        banking_service: BankingService,
    ):
        self.atm_session_repository = atm_session_repository
        self.banking_service = banking_service

    def execute(self, card_number: str, pin: str) -> bool:
        session = self.atm_session_repository.get_session(card_number)
        if not session:
            return False

        return self.atm_session_repository.enter_pin(session.current_card_number, pin)
