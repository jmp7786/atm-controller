class Account:
    def __init__(self, account_id, balance=0):
        self.account_id = account_id
        self.balance = balance

    def deposit(self, amount) -> bool:
        if amount > 0:
            self.balance += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        else:
            return False
