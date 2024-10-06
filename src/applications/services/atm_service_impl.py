from typing import List

from src.applications.interfaces.atm_service import ATMService
from src.applications.interfaces.use_cases.check_balance_use_case import \
    CheckBalanceUseCase
from src.applications.interfaces.use_cases.deposit_use_case import \
    DepositUseCase
from src.applications.interfaces.use_cases.eject_card_use_case import \
    EjectCardUseCase
from src.applications.interfaces.use_cases.enter_pin_use_case import \
    EnterPinUseCase
from src.applications.interfaces.use_cases.get_accounts_use_case import \
    GetAccountsUseCase
from src.applications.interfaces.use_cases.insert_card_use_case import \
    InsertCardUseCase
from src.applications.interfaces.use_cases.select_account_use_case import \
    SelectAccountUseCase
from src.applications.interfaces.use_cases.withdraw_use_case import \
    WithdrawUseCase
from src.applications.ports.secondary.account_repository import \
    AccountRepository
from src.applications.ports.secondary.cach_bin_port import CashBin
from src.domains.entities.account import Account
from src.mappers.account_mapper import AccountMapper


class ATMServiceImpl(ATMService):
    def __init__(
        self,
        account_mapper: AccountMapper,
        account_repository: AccountRepository,
        cash_bin: CashBin,
        insert_card_use_case: InsertCardUseCase,
        enter_pin_use_case: EnterPinUseCase,
        get_accounts_use_case: GetAccountsUseCase,
        select_account_use_case: SelectAccountUseCase,
        check_balance_use_case: CheckBalanceUseCase,
        deposit_use_case: DepositUseCase,
        withdraw_use_case: WithdrawUseCase,
        eject_card_use_case: EjectCardUseCase,
    ):
        self.account_mapper = account_mapper
        self.account_repository = account_repository
        self.cash_bin = cash_bin
        self.insert_card_use_case = insert_card_use_case
        self.enter_pin_use_case = enter_pin_use_case
        self.get_accounts_use_case = get_accounts_use_case
        self.select_account_use_case = select_account_use_case
        self.check_balance_use_case = check_balance_use_case
        self.deposit_use_case = deposit_use_case
        self.withdraw_use_case = withdraw_use_case
        self.eject_card_use_case = eject_card_use_case

    def insert_card(self, card_number: str) -> bool:
        return self.insert_card_use_case.execute(card_number)

    def enter_pin(self, card_number: str, pin: str) -> bool:
        return self.enter_pin_use_case.execute(card_number, pin)

    def get_accounts(self, card_number: str) -> List[Account]:
        return self.get_accounts_use_case.execute(card_number)

    def select_account(self, card_number: str, account_id: str):
        return self.select_account_use_case.execute(card_number, account_id)

    def check_balance(self, card_number: str) -> int:
        return self.check_balance_use_case.execute(card_number)

    def deposit(self, card_number: str, amount: int) -> bool:
        return self.deposit_use_case.execute(card_number, amount)

    def withdraw(self, card_number, amount) -> bool:
        return self.withdraw_use_case.execute(card_number, amount)

    def eject_card(self, card_number: str) -> bool:
        return self.eject_card_use_case.execute(card_number)
