import datetime
import sqlite3
import string
import random

from models.slips import TSlipsModel

def output_html():
    con = sqlite3.connect('database.sqlite3')
    slipsModel = TSlipsModel(con)
    category_amount_list = slipsModel.select_sum_amount_group_by_category()
    date_amount_list = slipsModel.select_sum_amount_group_by_transaction_date()
    con.close()

    with open('HTML/table_template.txt', encoding="utf-8") as f:
        table = string.Template(f.read())

    category_table_contents, category_labels, category_amount_data, color_list = category_html(category_amount_list, table)
    date_table_contents, date_list, d_amount_list = date_html(date_amount_list, table)

    with open('HTML/basehtml.txt', encoding="utf-8") as f:
        html = string.Template(f.read())

    output_html = html.substitute(category_amount_table=category_table_contents,
                                  category_labels=str(category_labels),
                                  category_color=str(color_list),
                                  category_amount=str(category_amount_data),
                                  date_amount_table=str(date_table_contents),
                                  date_labels=str(date_list),
                                  date_amount=str(d_amount_list))

    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S.html')
    with open('HTML/output/' + file_name, mode='w', encoding="utf8") as f:
        f.write(output_html)

def category_html(category_amount_list, table):
    contents = ''
    label_list = []
    amount_list = []
    color_list = []
    for category_amount in category_amount_list:
        category, amount = category_amount
        contents += table.substitute(
            type=category, amount="{:,}円".format(amount))+ '\n'

        label_list.append(category)
        amount_list.append(amount)
        color_list.append(
            "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))

    return (contents, label_list, amount_list, color_list)

def date_html(date_amount_list, table):
    contents = ''
    date_list = []
    amount_list = []
    for date_amount in date_amount_list:
        date, amount = date_amount
        contents += table.substitute(
            type=date, amount="{:,}円".format(amount)) + '\n'

        date_list.append(date)
        amount_list.append(amount)

    return (contents, date_list, amount_list)
