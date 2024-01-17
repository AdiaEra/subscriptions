import psycopg2.extras
from psycopg2.errors import UniqueViolation

from DB import conn


def add_user(user_name: str, chat_id: int):
    """
    Функция проверяет есть пользователь в базе, если нет, записывает в базу
    :param user_name: user_name пользователя
    :param chat_id: chat_id пользователя
    :return: Новый пользователь добавлен или Пользователь с таким user_name уже есть в базе
    """
    with conn.cursor() as cur:
        select_query = """SELECT user_name FROM users WHERE user_name = %s"""
        cur.execute(select_query, (user_name,))
        cur.fetchone()
        if cur.fetchone() is None:
            try:
                insert_query = """INSERT INTO users(user_name, chat_id)
                                  VALUES (%s, %s)"""
                cur.execute(insert_query, (user_name, chat_id))
            except UniqueViolation:
                return 'Пользователь с таким user_name уже есть в базе'
        return 'Новый пользователь добавлен'


us_name = 'Cate'
us_chat_id = 3333333333333
# print(add_user(us_name, us_chat_id))
conn.commit()


def list_chat_id():
    """
    Функция выдаёт список chat_id пользователей
    :return: список chat_id пользователей
    """
    with conn.cursor() as cur:
        cur.execute("""SELECT chat_id FROM users""")
        list_1 = [item for i in cur.fetchall() for item in i]
        return list_1


# print(list_chat_id())


def add_data(user_name: str, text: str, media: str, link: str, subscription_days: int):
    """
    Функция заполнения таблицы данных по подписке
    :param user_name: user_name пользователя
    :param text: текст
    :param media: изображение
    :param link: ссылка
    :param subscription_days: количество дней подписки
    :return:
    """
    with conn.cursor() as cur:
        insert_query = """INSERT INTO data_subscriptions(user_name, text, media, link, subscription_days)
                                          VALUES (%s, %s, %s, %s, %s)"""
        cur.execute(insert_query, (user_name, text, media, link, subscription_days))
        cur.execute("""SELECT subscription_days FROM data_subscriptions WHERE user_name = %s""", (user_name,))
        a = list(cur.fetchone())
        return f'Подписка оформлена {a} на дней'


us_name = 'Cate'
us_text = 'zdvd ggnghh hfthfth'
us_media = 'hgbwwyuyvyt'
us_link = 'qqqq@@@@@@@@@@@'
us_sub_days = 7
# print(add_data(us_name, us_text, us_media, us_link, us_sub_days))
conn.commit()


def update_subscription_days(user_name: str):
    """
    Функция уменьшает количество дней подписки на 1 и, если число равняется нулю, удаляет информацию по подписке.
    :param user_name: user_name пользователя
    :return: До окончания подписки осталось (количкство) дней
    """
    with conn.cursor() as cur:
        cur.execute("""UPDATE data_subscriptions SET subscription_days = subscription_days - 1 WHERE user_name = %s""",
                    (user_name,))
        cur.execute("""SELECT subscription_days FROM data_subscriptions WHERE user_name = %s""", (user_name,))
        a = list(cur.fetchone())
        cur.execute("""DELETE FROM data_subscriptions WHERE subscription_days = 0""")
        return f'До окончания подписки осталось {a} дней'


us_name = 'Cate'
# print(update_subscription_days(us_name))
conn.commit()


def data_output():
    """
    Функция выводит информацию из таблицы data_subscriptions
    :return: список словарей из таблицы data_subscriptions
    """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""SELECT * FROM data_subscriptions""")
        res = cur.fetchall()
        res_list = [dict(row) for row in res]
        return res_list


# print(data_output())

def data_output():
    """
    Функция выводит информацию из таблицы users
    :return: список словарей из таблицы users
    """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""SELECT * FROM users""")
        res = cur.fetchall()
        res_list = [dict(row) for row in res]
        return res_list


# print(data_output())


def delete_advertisement(user_name: str):
    """
    Функция удаляет объявление из таблицы data_subscriptions
    :param user_name: user name подписчика
    :return: подписка конкретного пользователя удалена
    """
    with conn.cursor() as cur:
        delete_query = """DELETE FROM data_subscriptions WHERE user_name = %s"""
        cur.execute(delete_query, (user_name,))
        return f'Подписка {user_name} удалена'


us_name = 'Cate'
# print(delete_advertisement(us_name))
conn.commit()


def output_subscription_days(user_name: str):
    """
    Функция выводит словарь с именем пользователя и количеством оставшихся дней подписки
    :param user_name: имя пользователя
    :return: словарь с именем пользователя и количеством оставшихся дней подписки
    """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""SELECT subscription_days FROM data_subscriptions WHERE user_name = %s""", (user_name,))
        res = cur.fetchall()
        res_list = [dict(row) for row in res]
        return res_list


us_name = 'Cate'
# print(output_subscription_days(us_name))