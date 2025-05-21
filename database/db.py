import psycopg2

conn = psycopg2.connect(
    dbname="ATM_app",
    user="ViraKrajevskiy",
    password="3003",
    host="localhost",
    port=5432
)

def init_db():
    cur = conn.cursor()

    # Создаем таблицу, если не существует
    cur.execute("""
CREATE TABLE IF NOT EXISTS money_nominal (
nominal INT PRIMARY KEY,
description TEXT NOT NULL
);
    """)

    # Вставляем данные, если их еще нет
    cur.execute("""
INSERT INTO money_nominal (nominal, description) VALUES
(1000, '1000 сум'),
(2000, '2000 сум'),
(5000, '5000 сум'),
(10000, '10000 сум'),
(20000, '20000 сум'),
(50000, '50000 сум'),
(100000, '100000 сум'),
(200000, '200000 сум')
ON CONFLICT (nominal) DO NOTHING;
    """)

    conn.commit()
    cur.close()

if __name__ == "__main__":
    init_db()
    conn.close()
    print("База инициализирована.")


def save_user_to_db(user: BaseUser, conn):
    """
Сохраняет объект BaseUser и связанные сущности в БД.
Требует, чтобы conn — активное соединение psycopg2.
    """
    cur = conn.cursor()

    try:
        # 1. Сохраняем пользователя
        cur.execute("""
INSERT INTO users (firstname, surname, lastname, phone_number, role_id, paper_money)
VALUES (%s, %s, %s, %s, %s, %s)
RETURNING user_id;
            """, (user.firstname, user.surname, user.lastname, user.phone.number, user.role_id, user.paper_money))

        user_id = cur.fetchone()[0]

        # 2. Сохраняем карту пользователя (CardMoney)
        # Предполагается, что у CardMoney есть атрибуты, например card_number, balance
        card = user.card
        cur.execute("""
INSERT INTO cards (user_id, card_number, balance)
VALUES (%s, %s, %s)
RETURNING card_id;
            """, (user_id, card.card_number, card.balance))

        card_id = cur.fetchone()[0]

        # 3. Сохраняем аккаунт, если есть
        if user.account:
            account = user.account
            cur.execute("""
INSERT INTO accounts (user_id, card_id)
VALUES (%s, %s)
RETURNING account_id;
                """, (user_id, card_id))

            account_id = cur.fetchone()[0]
        else:
            account_id = None

        # 4. Сохраняем наличные деньги (список объектов Money)
        for money_obj in user.wallet:
            # Предполагается, что Money хранит словарь номинал:кол-во в атрибуте money_dict
            for nominal, count in money_obj.money_dict.items():
                cur.execute("""
INSERT INTO money (user_id, nominal, count)
VALUES (%s, %s, %s)
ON CONFLICT (user_id, nominal) DO UPDATE SET count = excluded.count;
                    """, (user_id, nominal, count))

        conn.commit()
        print(f"Пользователь {user.firstname} успешно сохранён в БД.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при сохранении пользователя: {e}")
    finally:
        cur.close()
        