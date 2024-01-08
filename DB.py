import psycopg2

with psycopg2.connect(user="postgres",
                      password="Hun$917&305TpS",
                      port="5432",
                      database="subscriptions_db") as conn:
    def create_db():
        """
        Функция, создающая структуру БД (таблицы)
        :return: База данных создана
        """
        with conn.cursor() as cur:
            create_query = """ CREATE TABLE IF NOT EXISTS users(
                                user_name VARCHAR(20) PRIMARY KEY,
                                chat_id BIGINT
                                );
                                CREATE TABLE IF NOT EXISTS data_subscriptions(
                                id SERIAL PRIMARY KEY,
                                text TEXT,
                                media TEXT,
                                link TEXT,
                                subscription_days INTEGER,
                                user_name VARCHAR(20) REFERENCES users(user_name)
                                ON DELETE CASCADE
                                )"""
            cur.execute(create_query)
            return 'Таблицы созданы'


    # print(create_db())
    conn.commit()


    def delete_db():
        """
        Функция, удаляющая таблицы базы данных
        :return: База данных удалена
        """
        with conn.cursor() as cur:
            delete_query = """DROP TABLE data_subscriptions;
                DROP TABLE users
                CASCADE"""
            cur.execute(delete_query)
            return 'Таблицы удалены'


    # print(delete_db())
    conn.commit()
