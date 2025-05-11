class MoneyNominal:
    Money_nominal = {
        1000:"1000 сум",
        2000:"2000 сум",
        5000:"5000 сум",
        10000:"10000 сум",
        20000:"20000 сум",
        50000:"50000 сум",
        100000:"100000 сум",
        200000:"200000 сум"
    }

    @classmethod
    def get_money_nominal(cls, money_nomi):
        return cls.Money_nominal.get(money_nomi, "Неизвестный_номинал")




class CardMoney:
    def __init__(self, card_id, card_name, card_number, card_work_time, password, balance, card_type, phone_number):
        self.card_id = card_id
        self.card_name = card_name
        self.card_number = card_number
        self.card_work_time = card_work_time
        self.password = password
        self.balance = balance
        self.card_type = card_type
        self.phone_number = phone_number


class Money:
    # В этом классе теперь будем хранить все наличные деньги
    def __init__(self):
        self.money_list = []  # Список для хранения купюр

    def add_money(self, money_nomi, count):
        #Добавить деньги в кошелек, создавая новый объект Money для определенного номинала и количества
        money = {
            'money_nomi': money_nomi,
            'count': count,
            'money_name': MoneyNominal.get_money_nominal(money_nomi)
        }
        self.money_list.append(money)

    def total_balance(self):
        #Вычислить общий баланс наличных (сумма всех купюр в кошельке)
        total = 0
        for money in self.money_list:
            total += money['money_nomi'] * money['count']
        return total

    def __str__(self):
        #Показываем все деньги в кошельке
        money_info = "Наличные:\n"
        for money in self.money_list:
            money_info += f"- {money['count']} x {money['money_name']} = {money['money_nomi'] * money['count']} сум\n"
        return money_info


class Wallet:
    def __init__(self, card: CardMoney):
        self.card = card  # Привязываем карту к кошельку
        self.money = Money()  # Создаем объект Money для работы с наличными деньгами

    def add_cash(self, money_nomi, count):
        # Добавляем наличные деньги в кошелек
        self.money.add_money(money_nomi, count)

    def total_balance(self):
        # Получаем общий баланс наличных денег в кошельке
        return self.money.total_balance()

    def __str__(self):
        # Выводим информацию о кошельке (карту и наличные)
        return f"Карта: {self.card.card_name}\n" + str(self.money)
