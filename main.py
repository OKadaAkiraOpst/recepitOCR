import configparser
from PIL import Image
import re
 
import pyocr.builders
import pyocr
from models.logics.backlog_notifications import notify_backlog_issue
from models.logics.insert_slips import insert_sllips
from models.logics.output_html import output_html

if __name__ == '__main__':
    tools = pyocr.get_available_tools()
    tool = tools[0]
    
    langs = tool.get_available_languages()
    lang = langs[1]

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    txt = tool.image_to_string(
        Image.open(config['DEFAULT']['ReceiptUrl']),
        lang,
        builder=pyocr.builders.TextBuilder(
            tesseract_layout=config['DEFAULT']['TesseractLayout'])
    )

    txt = txt.replace(' ', '')

    # 店舗名の取得
    b_f_store_name = re.search('.*?店', txt)
    store_name = ''
    if b_f_store_name:
        store_name = re.sub('[\r\n|\n|\r]', ' ', b_f_store_name.group())

    # 購入日の取得
    purchase_date = re.search('\d{4}年\d{1,2}月\d{1,2}日', txt).group()

    # 不要な文字列を削除
    txt = re.sub('レジ.*', '', txt)
    txt = re.sub('\d{4}年\d{1,2}月\d{1,2}日.*', '', txt)
    txt = re.sub('.*?-\d+', '', txt)
    txt = re.sub('小計.+', '', txt)
    txt = re.sub('.*?\\\\\d+', '', txt)

    # 購入商品名と価格のリストを取得
    item_price_list = re.findall('^[\r\n|\n|\r]?(.*?[1-9]?\d+)$', txt, re.M)

    # 取引記録に保存
    insert_sllips(store_name, purchase_date, item_price_list)

    #HTML出力
    output_html()

    #BackLog通知
    if (bool(int(config['BACKLOG']['NotificationsFlag']))):
        notify_backlog_issue(config['BACKLOG']['Apikey'], config['BACKLOG']['IssueId'])
