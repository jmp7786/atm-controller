from typing import List

from src.applications.interfaces.use_cases.get_accounts_use_case import \
    GetAccountsUseCase
from src.applications.ports.secondary.account_repository import \
    AccountRepository
from src.applications.ports.secondary.atm_session_repository import \
    ATMSessionRepository
from src.applications.ports.secondary.banking_service_port import \
    BankingService
from src.domains.entities.account import Account


class GetAccountsUseCaseImpl(GetAccountsUseCase):
    def __init__(
        self,
        account_repository: AccountRepository,
        atm_session_repository: ATMSessionRepository,
        banking_service: BankingService,
    ):
        self.account_repository = account_repository
        self.atm_session_repository = atm_session_repository
        self.banking_service = banking_service

    def execute(self, card_number: str) -> List[Account]:
        session = self.atm_session_repository.get_session(card_number)
        if session and self.banking_service.validate_pin(session.current_card_number, session.pin):
            accounts = self.account_repository.get_accounts(card_number)
            if accounts:
                return list(accounts.values())

        return []
