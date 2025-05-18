from backend.classes.atm_class.ATM import Atm
from backend.classes.bank_class.Card_and_money import CardMoney
from backend.classes.bank_class.bank_worker import BankWorker
from backend.classes.collector.incosator import CashCollector
from backend.classes.user_class.users import Account, BaseUser


def save_user(cursor, user):
    cursor.execute("""
INSERT INTO users (firstname, surname, lastname, phone, paper_money, role_id, card_id)
VALUES (%s, %s, %s, %s, %s, %s, %s)
RETURNING id
        """, (user.firstname, user.surname, user.lastname, user.phone, user.paper_money, user.role_id, user.card.card_id))
    return cursor.fetchone()[0]

def save_card(cursor, card):
    cursor.execute("""
INSERT INTO cardmoney (card_id, card_name, card_number, card_work_time, password, balance, card_type, phone_number)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (card.card_id, card.card_name, card.card_number, card.card_work_time, card.password, card.balance, card.card_type, card.phone_number))

def save_money(cursor, money_dict, user_id):
    # money_dict: {'money_nomi': int, 'count': int}
    cursor.execute("""
INSERT INTO money (user_id, money_nomi, count)
VALUES (%s, %s, %s)
        """, (user_id, money_dict['money_nomi'], money_dict['count']))

def save_account(cursor, account, user_id):
    cursor.execute("""
INSERT INTO account (account_id, user_id, card_id)
VALUES (%s, %s, %s)
        """, (account.account_id, user_id, account.card.card_id))

def save_atm(cursor, atm):
    cursor.execute("""
INSERT INTO atm (balance, card_id, status_id)
VALUES (%s, %s, %s)
        """, (atm.balance, atm.card.card_id, atm.status_id))

def input_card(cursor):
    print("Создаём карту:")
    card_id = int(input("ID карты: "))
    card_name = input("Имя карты: ")
    card_number = input("Номер карты (16 цифр): ")
    card_work_time = input("Срок действия карты (например, 12/25): ")
    password = input("Пароль карты: ")
    balance = float(input("Баланс карты: "))
    card_type = input("Тип карты: ")
    phone_number = input("Телефон карты: ")

    card = CardMoney(card_id, card_name, card_number, card_work_time, password, balance, card_type, phone_number)
    save_card(cursor, card)
    return card

def input_wallet(cursor, user_id, card):
    wallet = []
    print("Добавляем наличные купюры (введите 0 в номинале для завершения):")
    while True:
        nomi = int(input("Номинал купюры: "))
        if nomi == 0:
            break
        count = int(input("Количество купюр: "))
        money_dict = {'money_nomi': nomi, 'count': count}
        wallet.append(money_dict)
        save_money(cursor, money_dict, user_id)
    return wallet

def input_account(cursor, user, card, wallet):
    account = Account(user, card, wallet)
    save_account(cursor, account, user_id=None)  # user_id не известен на момент создания, обновим позже
    return account

def create_base_user(cursor):
    print("Создаём обычного пользователя:")
    firstname = input("Имя: ")
    surname = input("Фамилия: ")
    lastname = input("Отчество: ")
    phone = input("Телефон: ")
    role_id = 1
    paper_money = float(input("Наличные (бумажные деньги): "))

    card = input_card(cursor)
    # Сохраним временно без user_id, т.к. пользователь ещё не создан
    user = BaseUser(firstname, surname, lastname, phone, paper_money, role_id, card, [], None)

    user_id = save_user(cursor, user)
    wallet = input_wallet(cursor, user_id, card)

    # Теперь создаём аккаунт с user
    account = Account(user, card, wallet)
    save_account(cursor, account, user_id)

    # Обновим user с аккаунтом и кошельком
    user.wallet = wallet
    user.account = account

    print(f"Пользователь создан с ID {user_id}")
    return user

def create_cash_collector(cursor):
    print("Создаём инкассатора:")
    firstname = input("Имя: ")
    surname = input("Фамилия: ")
    lastname = input("Отчество: ")
    phone = input("Телефон: ")
    role_id = 2

    card = input_card(cursor)
    wallet = []
    user = CashCollector(firstname, surname, lastname, phone, role_id, card, wallet)
    # Сохраняем пользователя
    user_id = save_user(cursor, user)
    wallet = input_wallet(cursor, user_id, card)
    user.wallet = wallet
    print(f"Инкассатор создан с ID {user_id}")
    return user

def create_bank_worker(cursor):
    print("Создаём работника банка:")
    firstname = input("Имя: ")
    surname = input("Фамилия: ")
    lastname = input("Отчество: ")
    phone = input("Телефон: ")
    role_id = 3

    card = input_card(cursor)
    wallet = []
    user = BankWorker(firstname, surname, lastname, phone, role_id, card, wallet)
    user_id = save_user(cursor, user)
    wallet = input_wallet(cursor, user_id, card)
    user.wallet = wallet
    print(f"Работник банка создан с ID {user_id}")
    return user

def create_atm(cursor):
    print("Создаём банкомат:")
    balance = int(input("Баланс банкомата: "))
    card = input_card(cursor)
    status_id = int(input("Статус (1 - Active, 2 - Not Active): "))
    atm = Atm(balance, card, status_id)
    save_atm(cursor, atm)
    print("Банкомат создан.")
    return atm

def main():
    import psycopg2
    conn = psycopg2.connect(dbname='your_db', user='your_user', password='your_pass', host='localhost')
    cursor = conn.cursor()

    try:
        user = create_base_user(cursor)
        collector = create_cash_collector(cursor)
        worker = create_bank_worker(cursor)
        atm = create_atm(cursor)

        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Ошибка:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
