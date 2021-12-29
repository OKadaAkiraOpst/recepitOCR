import sqlite3


class TItemCategoriesModel():

    def __init__(self, con: sqlite3.connect):
        self.cur = con.cursor()

    def select_all(self):
        query = "SELECT * FROM TRANSACTION_ITEMS_CATEGORIES"

        return self.cur.execute(query).fetchall()
