from src.applications.interfaces.use_cases.check_balance_use_case import \
    CheckBalanceUseCase
from src.applications.ports.secondary.account_repository import \
    AccountRepository
from src.applications.ports.secondary.atm_session_repository import \
    ATMSessionRepository
from src.applications.ports.secondary.banking_service_port import \
    BankingService


class CheckBalanceUseCaseImpl(CheckBalanceUseCase):
    def __init__(
        self,
        account_repository: AccountRepository,
        atm_session_repository: ATMSessionRepository,
        banking_service: BankingService,
    ):
        self.account_repository = account_repository
        self.atm_session_repository = atm_session_repository
        self.banking_service = banking_service

    def execute(self, card_number: str) -> int:
        session = self.atm_session_repository.get_session(card_number)
        if not session:
            return -1

        is_valid_pin = self.banking_service.validate_pin(session.current_card_number, session.pin)
        if not is_valid_pin:
            return -1

        account = self.account_repository.get_account(session.current_card_number, session.current_account_id)
        return account.balance
