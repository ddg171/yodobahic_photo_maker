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
        return []

    # タグIDそのままでは人が読めないのでデコードして
    # テーブルに格納する
    exif_table = {}
    
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = value

    data_requried=["Model","LensModel","ExposureTime","FNumber","ISOSpeedRatings","Orientation"]
    exif_data ={}
    for id in data_requried:
        try:
            if id =="Model" or id== "LensModel":
                exif_data[id]=exif_table[id]
            elif id=="ExposureTime":
                exif_data[id]=str(exif_table["ExposureTime"][0])+"/"+str(exif_table["ExposureTime"][1])
            elif id == "FNumber":
                exif_data[id]="F"+str(exif_table["FNumber"][0]/exif_table["FNumber"][1])
            elif id =="ISOSpeedRatings":
                exif_data[id]="ISO "+str(exif_table["ISOSpeedRatings"])
            #縦横判別情報も一緒に取り出しておく
            elif id == "Orientation":
                exif_data[id]=exif_table["Orientation"]
        except KeyError:
            pass
    return exif_data


if __name__ == "__main__":
    exif_data = get_exif_of_image("image\\sample3.JPG")
    pprint.pprint(exif_data)

#pyでの並びは(機種)(レンズ名)(シャッター速度)(絞り)(ISO感度)Photo by(撮影者名)
#レンズ一体型デジタルカメラは"LensModel"の項目がない。なのでKeyErrorが出る。
