from typing import List

from src.applications.services.atm_service_impl import ATMService
from src.domains.entities.account import Account


class ATMController:
    def __init__(self, atm_service: ATMService):
        self.atm_service = atm_service

    def insert_card(self, card_number: str):
        return self.atm_service.insert_card(card_number)

    def enter_pin(self, card_number: str, pin: str) -> bool:
        return self.atm_service.enter_pin(card_number, pin)

    def get_accounts(self, card_number: str) -> List[Account]:
        return self.atm_service.get_accounts(card_number)

    def select_account(self, card_number: str, account_id: str) -> bool:
        return self.atm_service.select_account(card_number, account_id)

    def check_balance(self, card_number: str) -> int:
        return self.atm_service.check_balance(card_number)

    def deposit(self, card_number: str, amount: int) -> bool:
        return self.atm_service.deposit(card_number, amount)

    def withdraw(self, card_number: str, amount: int) -> bool:
        return self.atm_service.withdraw(card_number, amount)

    def eject_card(self, card_number: str) -> bool:
        return self.atm_service.eject_card(card_number)
