class ATMSession:
    def __init__(self, card_number: str):
        self.current_card_number = card_number
        self.current_account_id = ""
        self.pin = ""
