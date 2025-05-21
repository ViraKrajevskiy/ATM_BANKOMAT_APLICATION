import re
import json
import sys
import os

from database import conn


class MoneyNominal:

    @classmethod
    def load_from_db(cls):
        cur = conn.cursor()
        cur.execute("SELECT nominal, description FROM money_nominal;")
        data = cur.fetchall()
        cur.close()
        cls.Money_nominal = {nominal: desc for nominal, desc in data}

    @classmethod
    def get_money_nominal(cls, money_nomi):
        return cls.Money_nominal.get(money_nomi, "Неизвестный номинал")

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

        # Валидация при создании
        self._validate_card_number()
        self._validate_phone_number()


    def _validate_card_number(self):
        # Проверяем, что номер карты состоит из 16 цифр
        if not (self.card_number.isdigit() and len(self.card_number) == 16):
            raise ValueError(f"Неверный номер карты: '{self.card_number}'. Должен быть из 16 цифр.")

    def _validate_phone_number(self):
        # Разрешаем телефон с + в начале и от 9 до 15 цифр, например +998901234567
        pattern = r'^\+?\d{9,15}$'
        if not re.match(pattern, self.phone_number):
            raise ValueError(f"Неверный номер телефона: '{self.phone_number}'. Формат: +123456789 или 123456789.")


def input_cardmoney():
    while True:
        try:
            card_id = int(input("Введите card_id (число): "))
            card_name = input("Введите card_name: ")
            card_number = input("Введите card_number: ")
            card_work_time = input("Введите card_work_time: ")
            password = input("Введите password: ")
            balance = float(input("Введите balance: "))
            card_type = input("Введите card_type: ")
            phone_number = input("Введите phone_number: ")

            # Попытка создать объект с валидацией
            card = CardMoney(card_id, card_name, card_number, card_work_time,
                             password, balance, card_type, phone_number)
            return card  # Если без ошибок, возвращаем объект

        except ValueError as e:
            print(f"Ошибка ввода: {e}. Попробуйте еще раз.\n")


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


def input_wallet(card: CardMoney):
    wallet = Wallet(card)
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
            wallet.add_cash(money_nomi, count)
        except ValueError:
            print("Ошибка ввода. Повторите.")

    return wallet






