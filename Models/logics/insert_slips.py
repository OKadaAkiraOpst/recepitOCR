import configparser
import re
import sqlite3

from models.item_categories import TItemCategoriesModel
from models.slips import TSlipsModel


def insert_sllips(store_name, purchase_date, item_price_list):
    con = sqlite3.connect('database.sqlite3')
    try:
        item_categories_model = TItemCategoriesModel(con)
        item_category_list = item_categories_model.select_all()
        slips_model = TSlipsModel(con)

        for item_price in item_price_list:
            price = re.search('\d+$', item_price).group()
            name = re.sub('\d+$', '', item_price)
            category = match_category(name, item_category_list)

            slips_model.insert(
                (store_name, name, purchase_date, price, category))

        con.commit()
    except sqlite3.Error as e:
        print(e)
        con.rollback()
    finally:
        con.close()

def match_category(item_name, category_list):
        category = 62
        for item_category in category_list:
            _, n, c = item_category
            if n in item_name:
                category = c
                break

        return category
