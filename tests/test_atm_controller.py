import unittest

from src.adapters.primary.atm_controller import ATMController
from src.adapters.secondary.account_repository_impl import \
    AccountRepositoryImpl
from src.adapters.secondary.atm_session_repository_impl import \
    ATMSessionRepositoryImpl
from src.adapters.secondary.cash_bin_impl import CashBinImpl
from src.applications.services.atm_service_impl import ATMServiceImpl
from src.applications.usecases.check_balance_use_case import \
    CheckBalanceUseCaseImpl
from src.applications.usecases.deposit_use_case import DepositUseCaseImpl
from src.applications.usecases.eject_card_use_case import EjectCardUseCaseImpl
from src.applications.usecases.enter_pin_use_case import EnterPinUseCaseImpl
from src.applications.usecases.get_accounts_use_case import \
    GetAccountsUseCaseImpl
from src.applications.usecases.insert_card_use_case import \
    InsertCardUseCaseImpl
from src.applications.usecases.select_account_use_case import \
    SelectAccountUseCaseImpl
from src.applications.usecases.withdraw_use_case import WithdrawUseCaseImpl
from src.domains.entities.account import Account
from src.mappers.account_mapper import AccountMapper
from tests.mocks.mock_banking_service import MockBankingService


class TestATMController(unittest.TestCase):
    def setUp(self):
        self.card_number = "1234567890"
        self.invalid_card_number = "0000000000"
        self.pin = "1234"
        self.invalid_pin = "0000"
        self.account_id = "acc123"
        self.invalid_account_id = "acc999"
        self.initial_balance = 500

        cards_pins = {
            self.invalid_card_number: self.invalid_pin,
            self.card_number: self.pin,
        }

        self.atm_session_repository = ATMSessionRepositoryImpl()
        self.account_mapper = AccountMapper()
        self.account_repository = AccountRepositoryImpl(self.account_mapper)
        self.cash_bin = CashBinImpl(total_cash=1000)
        self.banking_service = MockBankingService(cards_pins)

        self.insert_card_use_case = InsertCardUseCaseImpl(self.atm_session_repository)
        self.enter_pin_use_case = EnterPinUseCaseImpl(self.atm_session_repository, self.banking_service)
        self.get_accounts_use_case = GetAccountsUseCaseImpl(
            self.account_repository, self.atm_session_repository, self.banking_service
        )
        self.select_account_use_case = SelectAccountUseCaseImpl(
            self.account_repository, self.atm_session_repository, self.banking_service
        )
        self.check_balance_use_case = CheckBalanceUseCaseImpl(
            self.account_repository, self.atm_session_repository, self.banking_service
        )
        self.deposit_use_case = DepositUseCaseImpl(
            self.account_repository,
            self.atm_session_repository,
            self.cash_bin,
            self.banking_service,
        )
        self.withdraw_use_case = WithdrawUseCaseImpl(
            self.account_repository,
            self.atm_session_repository,
            self.cash_bin,
            self.banking_service,
        )
        self.eject_card_use_case = EjectCardUseCaseImpl(self.atm_session_repository)

        self.atm_service = ATMServiceImpl(
            account_mapper=self.account_mapper,
            account_repository=self.account_repository,
            cash_bin=self.cash_bin,
            insert_card_use_case=self.insert_card_use_case,
            enter_pin_use_case=self.enter_pin_use_case,
            get_accounts_use_case=self.get_accounts_use_case,
            select_account_use_case=self.select_account_use_case,
            check_balance_use_case=self.check_balance_use_case,
            deposit_use_case=self.deposit_use_case,
            withdraw_use_case=self.withdraw_use_case,
            eject_card_use_case=self.eject_card_use_case,
        )

        self.atm_controller = ATMController(self.atm_service)

        account = Account(account_id=self.account_id, balance=self.initial_balance)
        self.account_repository.storage = {self.card_number: {self.account_id: account}}

    def test_full_atm_flow(self):
        self.atm_controller.insert_card(self.card_number)
        session = self.atm_session_repository.get_session(self.card_number)
        self.assertIsNotNone(session, "Session should be created after inserting card.")

        pin_valid = self.atm_controller.enter_pin(self.card_number, self.pin)
        self.assertTrue(pin_valid, "PIN should be valid.")

        accounts = self.atm_controller.get_accounts(self.card_number)
        self.assertIsNotNone(accounts, "Should retrieve accounts.")
        self.assertIn(
            self.account_id,
            [acc.account_id for acc in accounts],
            "Account ID should be primary accounts list.",
        )

        account_selected = self.atm_controller.select_account(self.card_number, self.account_id)
        self.assertTrue(account_selected, "Account should be successfully selected.")

        balance = self.atm_controller.check_balance(self.card_number)
        self.assertEqual(balance, self.initial_balance, "Balance should match initial balance.")

        deposit_amount = 100
        deposit_success = self.atm_controller.deposit(self.card_number, deposit_amount)
        self.assertTrue(deposit_success, "Deposit should be successful.")
        balance_after_deposit = self.atm_controller.check_balance(self.card_number)
        self.assertEqual(
            balance_after_deposit,
            self.initial_balance + deposit_amount,
            "Balance should reflect deposit.",
        )

        withdraw_amount = 200
        withdraw_success = self.atm_controller.withdraw(self.card_number, withdraw_amount)
        self.assertTrue(withdraw_success, "Withdrawal should be successful.")
        balance_after_withdraw = self.atm_controller.check_balance(self.card_number)
        self.assertEqual(
            balance_after_withdraw,
            balance_after_deposit - withdraw_amount,
            "Balance should reflect withdrawal.",
        )

        self.atm_controller.eject_card(self.card_number)
        session_after_eject = self.atm_session_repository.get_session(self.card_number)
        self.assertIsNone(session_after_eject, "Session should be terminated after ejecting card.")

    def test_invalid_pin(self):
        self.atm_controller.insert_card(self.card_number)

        invalid_pin = "0000"
        self.atm_controller.enter_pin(self.card_number, invalid_pin)
        check_balance_with_invalid_pin = self.atm_controller.check_balance(self.card_number)
        self.assertTrue(check_balance_with_invalid_pin == -1, "PIN should be invalid.")

    def test_insufficient_funds(self):
        self.atm_controller.insert_card(self.card_number)
        self.atm_controller.enter_pin(self.card_number, self.pin)
        self.atm_controller.select_account(self.card_number, self.account_id)

        withdraw_amount = self.initial_balance + 100
        withdrew_success = self.atm_controller.withdraw(self.card_number, withdraw_amount)
        self.assertFalse(withdrew_success, "Withdrawal should fail due to insufficient funds.")

    def test_cash_bin_limits(self):
        self.cash_bin.total_cash = 50

        self.atm_controller.insert_card(self.card_number)
        self.atm_controller.enter_pin(self.card_number, self.pin)
        self.atm_controller.select_account(self.card_number, self.account_id)

        withdraw_amount = 100
        withdrew_success = self.atm_controller.withdraw(self.card_number, withdraw_amount)
        self.assertFalse(withdrew_success, "Withdrawal should fail due to cash bin limit.")

        withdraw_amount = 50
        withdrew = self.atm_controller.withdraw(self.card_number, withdraw_amount)
        self.assertTrue(withdrew, "Withdrawal should succeed within cash bin limit.")

    def test_concurrent_sessions(self):
        card_number_2 = "0987654321"
        account_id_2 = "acc456"
        initial_balance_2 = 300

        account_2 = Account(account_id=account_id_2, balance=initial_balance_2)
        self.account_repository.storage[card_number_2] = {account_id_2: account_2}

        self.atm_controller.insert_card(self.card_number)
        self.atm_controller.enter_pin(self.card_number, self.pin)
        self.atm_controller.select_account(self.card_number, self.account_id)

        self.atm_controller.insert_card(card_number_2)
        self.atm_controller.enter_pin(card_number_2, self.pin)
        self.atm_controller.select_account(card_number_2, account_id_2)

        balance1 = self.atm_controller.check_balance(self.card_number)
        self.assertEqual(balance1, self.initial_balance, "First account balance should be correct.")

        balance2 = self.atm_controller.check_balance(card_number_2)
        self.assertEqual(balance2, initial_balance_2, "Second account balance should be correct.")

    def test_negative_amount_operations(self):
        self.atm_controller.insert_card(self.card_number)
        self.atm_controller.enter_pin(self.card_number, self.pin)
        self.atm_controller.select_account(self.card_number, self.account_id)

        deposit_success = self.atm_controller.deposit(self.card_number, -100)
        self.assertFalse(deposit_success, "Should not allow deposit of negative amount.")

        withdrew_success = self.atm_controller.withdraw(self.card_number, -100)
        self.assertFalse(withdrew_success, "Should not allow withdrawal of negative amount.")

    def test_select_invalid_account(self):
        self.atm_controller.insert_card(self.card_number)
        self.atm_controller.enter_pin(self.card_number, self.pin)

        account_selected = self.atm_controller.select_account(self.card_number, self.invalid_account_id)
        self.assertFalse(account_selected, "Should not select invalid account.")

    def test_operations_without_authentication(self):
        balance = self.atm_controller.check_balance(self.card_number)
        self.assertEqual(balance, -1, "Should not allow checking balance without authentication.")

        deposit_success = self.atm_controller.deposit(self.card_number, 100)
        self.assertFalse(deposit_success, "Should not allow deposit without authentication.")

        withdrew_success = self.atm_controller.withdraw(self.card_number, 100)
        self.assertFalse(withdrew_success, "Should not allow withdrawal without authentication.")

    def test_invalid_card_number(self):
        self.atm_controller.insert_card(self.invalid_card_number)
        session = self.atm_session_repository.get_session(self.invalid_card_number)
        self.assertIsNotNone(session, "Session should be created even for invalid card numbers.")

        self.atm_controller.enter_pin(self.invalid_card_number, self.pin)
        check_balance_with_invalid_card_number = self.atm_controller.check_balance(self.invalid_card_number)
        self.assertTrue(check_balance_with_invalid_card_number == -1, "PIN should be invalid.")

    def test_withdraw_exact_balance(self):
        self.atm_controller.insert_card(self.card_number)
        self.atm_controller.enter_pin(self.card_number, self.pin)
        self.atm_controller.select_account(self.card_number, self.account_id)

        withdraw_amount = self.initial_balance
        withdraw_success = self.atm_controller.withdraw(self.card_number, withdraw_amount)
        self.assertTrue(withdraw_success, "Withdrawal of exact balance should succeed.")

        balance_after_withdraw = self.atm_controller.check_balance(self.card_number)
        self.assertEqual(
            balance_after_withdraw,
            0,
            "Balance should be zero after withdrawing all funds.",
        )

    def test_withdraw_exact_cash_bin_amount(self):
        self.cash_bin.total_cash = 300

        self.atm_controller.insert_card(self.card_number)
        self.atm_controller.enter_pin(self.card_number, self.pin)
        self.atm_controller.select_account(self.card_number, self.account_id)

        withdraw_amount = 300
        withdraw_success = self.atm_controller.withdraw(self.card_number, withdraw_amount)
        self.assertTrue(withdraw_success, "Withdrawal of exact cash bin amount should succeed.")

        self.assertEqual(self.cash_bin.total_cash, 0, "Cash bin should be empty after withdrawal.")

    def test_withdraw_when_balance_zero(self):
        self.account_repository.storage[self.card_number][self.account_id].balance = 0

        self.atm_controller.insert_card(self.card_number)
        self.atm_controller.enter_pin(self.card_number, self.pin)
        self.atm_controller.select_account(self.card_number, self.account_id)

        withdraw_amount = 1
        withdraw_success = self.atm_controller.withdraw(self.card_number, withdraw_amount)
        self.assertFalse(withdraw_success, "Withdrawal should fail when balance is zero.")

    def test_withdraw_minimum_amount(self):
        self.atm_controller.insert_card(self.card_number)
        self.atm_controller.enter_pin(self.card_number, self.pin)
        self.atm_controller.select_account(self.card_number, self.account_id)

        withdraw_amount = 1
        withdraw_success = self.atm_controller.withdraw(self.card_number, withdraw_amount)
        self.assertTrue(withdraw_success, "Withdrawal of minimum amount should succeed.")

        balance_after_withdraw = self.atm_controller.check_balance(self.card_number)
        self.assertEqual(
            balance_after_withdraw,
            self.initial_balance - 1,
            "Balance should decrease by minimum amount.",
        )

    def test_select_account_without_pin(self):
        self.atm_controller.insert_card(self.card_number)
        account_selected = self.atm_controller.select_account(self.card_number, self.account_id)
        self.assertFalse(
            account_selected,
            "Should not allow account selection without PIN authentication.",
        )

    def test_withdraw_with_no_cash_in_bin(self):
        self.cash_bin.total_cash = 0

        self.atm_controller.insert_card(self.card_number)
        self.atm_controller.enter_pin(self.card_number, self.pin)
        self.atm_controller.select_account(self.card_number, self.account_id)

        withdraw_amount = 100
        withdraw_success = self.atm_controller.withdraw(self.card_number, withdraw_amount)
        self.assertFalse(
            withdraw_success,
            "Withdrawal should fail when cash bin is empty, even if balance is sufficient.",
        )
