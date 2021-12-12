import sqlite3

class TCategoriesModel():

    def __init__(self, con):
        cur = con.cursor()