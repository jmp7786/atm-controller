from typing import Optional

from src.applications.ports.secondary.account_repository import \
    AccountRepository
from src.domains.entities.account import Account
from src.mappers.account_mapper import AccountMapper


class AccountRepositoryImpl(AccountRepository):
    def __init__(self, mapper: AccountMapper):
        self.storage: dict[str: dict[str, Account]] = {}
        self.mapper = mapper

    def get_account(self, card_number: str, account_id: str) -> Optional[Account]:
        accounts = self.storage.get(card_number)
        if accounts:
            account = accounts.get(account_id)
            if account:
                return self.mapper.to_domain(account)
        return None

    def get_accounts(self, card_number: str) -> Optional[dict[str, Account]]:
        return self.storage.get(card_number)

    def save(self, card_number: str, account: Account) -> bool:
        account_entity = self.mapper.to_entity(account)
        self.storage[card_number][account_entity.account_id] = account_entity
        return True
