import sqlite3


class TSlipsModel():
    def __init__(self, con):
        self.cur = con.cursor()

    def insert(self, slips):
        query = """INSERT INTO TRANSACTION_SLIPS 
                (STORE_NAME, TRANSACTION_DESCRIPTION,
                TRANSACTION_DATE, TRANSACTION_AMOUNT,
                TRANSACTION_CATEGORY_ID)
            VALUES
                (?, ?, ?, ?, ?)"""

        self.cur.execute(query, slips)
