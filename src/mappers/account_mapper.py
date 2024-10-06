from src.domains.entities.account import Account
from src.entities.account_entity import AccountEntity


class AccountMapper:
    def to_domain(self, entity: AccountEntity) -> Account:
        return Account(account_id=entity.account_id, balance=entity.balance)

    def to_entity(self, account: Account) -> AccountEntity:
        return AccountEntity(account_id=account.account_id, balance=account.balance)
