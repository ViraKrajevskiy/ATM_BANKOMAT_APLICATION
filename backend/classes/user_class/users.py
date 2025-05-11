from itertools import count

from backend.classes.bank_class.Card_and_money import CardMoney, Money

class Role:
    roles = {
        1: "Обычный_пользователь",
        2: "Инкассатор",
        3: "Работник_банка"
    }

    @classmethod
    def get_role_name(cls, role_id):
        return cls.roles.get(role_id, "Неизвестная_роль")

class Account:
    _id_counter = count(1)

    def __init__(self, user, card: CardMoney, wallet: list[Money]):
        if user.role_id != 1:
            raise ValueError("Только обычный пользователь может иметь Account")
        self.account_id = next(Account._id_counter)
        self.user = user
        self.card = card
        self.wallet = wallet

    def total_cash(self):
        return sum(m.total_balance() for m in self.wallet)

    def __str__(self):
        return (f"Аккаунт #{self.account_id} — {self.user.firstname} {self.user.surname} ({self.user.role})\n"
                f"Баланс карты: {self.card.balance} сум\n"
                f"Наличные: {self.total_cash()} сум")

class BaseUser:
    def __init__(self, firstname, surname, lastname, phone, paper_money, role_id, card: CardMoney, wallet: list[Money], account: Account):
        if role_id not in Role.roles:
            raise ValueError(f"Неверный role_id: {role_id}. Допустимые значения: {list(Role.roles.keys())}")

        self.firstname = firstname
        self.surname = surname
        self.lastname = lastname
        self.phone = phone
        self.role_id = role_id
        self.paper_money = paper_money
        self.role = Role.get_role_name(role_id)

        self.card = card
        self.wallet = wallet
        self.account = account

    def __str__(self):
        return f"{self.firstname} {self.surname} ({self.role})"

    def user_permissions(self):
        pass

    def total_balance(self):
        return self.paper_money + self.card.balance + sum(m.total_balance() for m in self.wallet)



    