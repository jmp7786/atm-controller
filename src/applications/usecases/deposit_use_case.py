from src.applications.interfaces.use_cases.deposit_use_case import \
    DepositUseCase
from src.applications.ports.secondary.account_repository import \
    AccountRepository
from src.applications.ports.secondary.atm_session_repository import \
    ATMSessionRepository
from src.applications.ports.secondary.banking_service_port import \
    BankingService
from src.applications.ports.secondary.cach_bin_port import CashBin


class DepositUseCaseImpl(DepositUseCase):
    def __init__(
        self,
        account_repository: AccountRepository,
        atm_session_repository: ATMSessionRepository,
        cash_bin: CashBin,
        banking_service: BankingService,
    ):
        self.account_repository = account_repository
        self.atm_session_repository = atm_session_repository
        self.cash_bin = cash_bin
        self.banking_service = banking_service

    def execute(self, card_number: str, amount: int) -> bool:
        session = self.atm_session_repository.get_session(card_number)
        if session and self.banking_service.validate_pin(session.current_card_number, session.pin):
            account = self.account_repository.get_account(session.current_card_number, session.current_account_id)
            if account:
                deposit_result = account.deposit(amount)
                if deposit_result:
                    return self.account_repository.save(card_number, account)

        return False
