from src.applications.ports.secondary.banking_service_port import \
    BankingService


class MockBankingService(BankingService):
    def __init__(self, cards_pins: dict[str, str]):
        self.cards_pins = cards_pins

    def validate_pin(self, card_number, pin):
        if card_number in self.cards_pins:
            return self.cards_pins[card_number] == pin
        else:
            return "1234" == pin
