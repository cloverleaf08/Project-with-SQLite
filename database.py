import sqlite3

class Database():

    def __init__(self):
        self.db = sqlite3.connect("database.db")
        self.cursor = self.db.cursor()


    def create_table_users(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INT,
            full name VARCHAR(221)
        )""")
        self.db.commit()


    def add_user(self, user_id, user_full_name):
        self.cursor.execute("""
        INSERT INTO users (id, full_name) VALUES (?, ?)
        """, (user_id, user_full_name))
        self.db.commit()


    def select_user(self):
        user_select = self.cursor.execute("""
        select * from users""")
        return user_select.fetchall()

    def close_database(self):
        self.db.close()



