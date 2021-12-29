from datetime import datetime
from sqlite3.dbapi2 import Date
from PIL import Image
import sys
import sqlite3
import re
 
import pyocr.builders
import pyocr
from models.item_categories import TItemCategoriesModel

from models.slips import TSlipsModel

if __name__ == '__main__':
    # pyocr自体が入っているかどうかと、利用できる文字認識エンジンを確認
    # get_available_tools()で利用できる文字認識エンジンを返します。
    tools = pyocr.get_available_tools()
    print(tools)
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    # Tesseractしか文字認識エンジンを入れていない場合は、当然最初の要素がTesseractになりますが、
    # 複数入れている場合は変わります。状況に応じてコードは変えましょう。
    tool = tools[0]
    print("Will use tool '%s'" % (tool.get_name()))
    
    # その文字認識エンジンで利用できる言語リストを取り出します。
    langs = tool.get_available_languages()
    print("Available languages: %s" % ", ".join(langs))
    lang = langs[1]
    print("Will use lang '%s'" % (lang))

    txt = tool.image_to_string(
        Image.open('receipts/receipt2.jpg'),
        lang="jpn",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )

    txt = txt.replace(' ', '')

    b_f_store_name = re.search('.*?店', txt)
    store_name = ''
    if b_f_store_name:
        store_name = re.sub('[\r\n|\n|\r]', ' ', b_f_store_name.group())

    print(store_name)

    purchase_date = re.search('\d{4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{1,2}', txt).group()
    print(purchase_date)

    txt = re.sub('小計.+', '', txt)
    txt = re.sub('.*?\\\\\d+', '', txt)
    item_price_list = re.findall('^[\r\n|\n|\r]?(\D+[1-9]+\d+)$', txt, re.M)

    con = sqlite3.connect('database.sqlite3')
    try:
        item_categories_model = TItemCategoriesModel(con)
        item_category_list = item_categories_model.select_all()
        slips_model = TSlipsModel(con)
        for item_price in item_price_list:
            name = re.match('^\D+', item_price).group()
            price = re.search('\d+$', item_price).group()
            category = 62
            for item_category in item_category_list:
                _, n, c = item_category
                if n in name:
                    category = c
                    break
            
            slips_model.insert((store_name, name, purchase_date, price, category))

        con.commit()
    except sqlite3.Error as e:
        print(e)
        con.rollback()
    finally:
        con.close()
