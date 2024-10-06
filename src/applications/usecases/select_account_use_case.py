from src.applications.interfaces.use_cases.select_account_use_case import \
    SelectAccountUseCase
from src.applications.ports.secondary.atm_session_repository import \
    ATMSessionRepository
from src.applications.ports.secondary.banking_service_port import \
    BankingService


class SelectAccountUseCaseImpl(SelectAccountUseCase):
    def __init__(
        self,
        account_repository,
        atm_session_repository: ATMSessionRepository,
        banking_service: BankingService,
    ):
        self.account_repository = account_repository
        self.atm_session_repository = atm_session_repository
        self.banking_service = banking_service

    def execute(self, card_number: str, account_id: str) -> bool:
        session = self.atm_session_repository.get_session(card_number)

        if not session:
            return False

        is_valid_pin = self.banking_service.validate_pin(session.current_card_number, session.pin)
        if not is_valid_pin:
            return False

        account = self.account_repository.get_account(card_number, account_id)
        if account:
            return self.atm_session_repository.select_account(session.current_card_number, account.account_id)
        else:
            return False
