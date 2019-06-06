#coding UTF-8

from PIL import Image
from PIL.ExifTags import TAGS
import pprint


def get_exif_of_image(file):
    """Get EXIF of an image if exists.

    指定した画像のEXIFデータを取り出す関数
    @return exif_table Exif データを格納した辞書
    """
    im = Image.open(file)

    # Exif データを取得
    # 存在しなければそのまま終了 空の辞書を返す
    try:
        exif = im._getexif()
    except AttributeError:
        return {}
    

    # タグIDそのままでは人が読めないのでデコードして
    # テーブルに格納する
    exif_table = {}
    
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = value

    return exif_table

exif_data = get_exif_of_image("sample.jpg")

#pprint.pprint(exif_data)


photo_info =[exif_data["Model"],exif_data["LensModel"],str(exif_data["ExposureTime"][0])+"/"+str(exif_data["ExposureTime"][1]),"F"+str(exif_data["FNumber"][0]/exif_data["FNumber"][1]),"ISO "+str(exif_data["ISOSpeedRatings"])]

pprint.pprint(photo_info)
#pyでの並びは(機種)(レンズ名)(シャッター速度)(絞り)(ISO感度)Photo by(撮影者名)str(exif_data["ExposureTime"][0])