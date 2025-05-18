from itertools import count

from backend.classes.bank_class.Card_and_money import CardMoney, Money, input_cardmoney, MoneyNominal


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



def input_money():
    money = Money()
    print("Добавление наличных купюр. Для окончания введите пустой номинал.")

    while True:
        money_nomi_input = input("Введите номинал купюры (например, 1000): ")
        if money_nomi_input == "":
            break
        try:
            money_nomi = int(money_nomi_input)
            if money_nomi not in MoneyNominal.Money_nominal:
                print("Номинал неизвестен. Попробуйте еще раз.")
                continue
            count = int(input("Введите количество купюр данного номинала: "))
            if count < 0:
                print("Количество не может быть отрицательным.")
                continue
            money.add_money(money_nomi, count)
        except ValueError:
            print("Ошибка ввода. Повторите.")
    return money

def input_baseuser():
    while True:
        try:
            firstname = input("Введите имя: ")
            surname = input("Введите фамилию: ")
            lastname = input("Введите отчество: ")
            phone = input("Введите телефон: ")

            # Роль
            print("Выберите роль:")
            for k, v in Role.roles.items():
                print(f"{k} - {v}")
            role_id = int(input("Введите номер роли: "))
            if role_id not in Role.roles:
                print("Неверная роль. Попробуйте снова.")
                continue

            # Создаем карту с валидацией
            card = input_cardmoney()

            # Создаем наличные деньги
            cash = input_money()

            # Создаем кошелек как список наличных (если нужно, можно расширить)
            wallet = [cash]

            # Создаем аккаунт — только если роль 1
            account = None
            if role_id == 1:
                account = Account(user=BaseUser.__new__(BaseUser), card=card, wallet=wallet)
                # Чтобы не создавать рекурсию, используем __new__, потом инициализируем
                # Но проще сначала создать user без аккаунта, потом добавить аккаунт
            user = BaseUser(firstname, surname, lastname, phone, cash.total_balance(), role_id, card, wallet, account)

            # Если роль 1, то обновим account.user на созданного пользователя
            if role_id == 1:
                user.account.user = user

            return user
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.\n")

    