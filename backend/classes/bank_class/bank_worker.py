from backend.classes.bank_class.Card_and_money import Money, CardMoney
from backend.classes.user_class.users import Role


class BankWorker:
    def __init__(self, firstname, surname, lastname, phone, role_id, card: CardMoney, wallet: list[Money]):
        if role_id != 3:
            raise ValueError("Только работник банка может быть BankWorker (role_id должен быть 3)")

        self.firstname = firstname
        self.surname = surname
        self.lastname = lastname
        self.phone = phone
        self.role_id = role_id
        self.role = Role.get_role_name(role_id)

        self.card = card
        self.wallet = wallet

    def __str__(self):
        return f"{self.firstname} {self.surname} ({self.role})"

    def total_balance(self):
        return self.card.balance + sum(m.total_balance() for m in self.wallet)

    def user_permissions(self):
        return "Может пополнять банкомат, просматривать состояние банкоматов и управлять ими"
