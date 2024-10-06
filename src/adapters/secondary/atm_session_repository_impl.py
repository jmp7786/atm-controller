# core/in_memory_atm_session_repo.py

from typing import Optional

from src.applications.ports.secondary.atm_session_repository import \
    ATMSessionRepository
from src.entities.atm_session import ATMSession


class ATMSessionRepositoryImpl(ATMSessionRepository):
    def __init__(self):
        self.sessions = {}

    def create_session(self, card_number: str) -> bool:
        self.sessions[card_number] = ATMSession(card_number)
        return True

    def get_session(self, card_number: str) -> Optional[ATMSession]:
        return self.sessions.get(card_number)

    def delete_session(self, card_number: str) -> bool:
        if card_number in self.sessions:
            del self.sessions[card_number]
            return True
        return False

    def select_account(self, card_number: str, account_id: str) -> bool:
        session = self.sessions.get(card_number)
        if session:
            session.current_account_id = account_id
            return True
        return False

    def enter_pin(self, card_number: str, pin: str) -> bool:
        session = self.sessions.get(card_number)
        if session:
            session.pin = pin
            return True
        return False

    def eject_card(self, card_number: str) -> bool:
        del self.sessions[card_number]
        return True
