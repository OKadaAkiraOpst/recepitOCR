from PIL import Image
import sys
 
import pyocr.builders
import pyocr

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
print(txt)
