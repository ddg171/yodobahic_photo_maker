#coding UTF-8

import re
import os
import datetime

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL.ExifTags import TAGS

def get_exif_of_image(file):
    data_requried=["Model","LensModel","ExposureTime","FNumber","ISOSpeedRatings"]
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
    try:
        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            exif_table[tag] = value
    except AttributeError:
        pass

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
        except KeyError:
            pass
    return exif_data


def photo_info_to_str(name,**exif_data):
    #取り出したEXIF情報を一つの文字列にまとめる
    #レンズの製品名の後ろに括弧付きで型番がついている場合は削除する
    try:
        exif_data["LensModel"]=re.sub(r"\s?[(].+[)]","",exif_data["LensModel"])
    except KeyError:
        pass
    #pyでの並びは(機種)(レンズ名)(シャッター速度)(絞り)(ISO感度)Photo by(撮影者名)
    info_requried=["Model","LensModel","ExposureTime","FNumber","ISOSpeedRatings"]
    exif_str=""
    for id in info_requried:
        try:
            exif_str += exif_data[id]+","
        except KeyError:
            pass
    if name =="":
        exif_str=exif_str[:-1]
    else:
        exif_str +="Photo by "+name
    return exif_str

def color_check(image_cropped):
    #文字の背景に合わせて文字色を決める
    threshold =240
    color_white =(240,240,240,100)
    color_black =(20,20,20,100)
    image_cropped.convert("RGB")
    red_list=[]
    green_list=[]
    blue_list=[]
    for y in range(image_cropped.height):
        for x in range(image_cropped.width):
            red,green,blue = image_cropped.getpixel((x,y))
            red_list.append(red)
            green_list.append(green)
            blue_list.append(blue)

    red_ave =sum(red_list)/len(red_list)
    green_ave=sum(green_list)/len(green_list)
    blue_ave=sum(blue_list)/len(blue_list)
    ave=(red_ave+green_ave+blue_ave)/3

    if ave>threshold:
        return color_black
    else:
        return color_white


def write_to_image(image_path,text):
    font_path = "font\meiryo.ttc"
    #文字列を画像に書き込む
    image =Image.open(image_path)
    font_size =int(0.016*image.height)
    margin =font_size
    font =ImageFont.truetype(font_path,font_size)
    draw = ImageDraw.Draw(image)
    #文字数に応じて位置を調整する
    if draw.textsize(text,font)[0]+margin>image.width:
        while draw.textsize(text+"...",font)[0]>image.width-margin:
            text= text[:-1]
        text=text+"..."
    text_width= draw.textsize(text,font)[0]
    draw_x=image.width-(text_width+margin)
    draw_y = image.height-(font_size+margin)

    #背景に合わせて文字色を変更する
    color = color_check(image.crop((draw_x,draw_y,image.width,image.height)))

    draw.text((draw_x, draw_y), text, font=font, fill=color)
    return image

def resize_for_web(image,resize_height):
    #指定した縦解像度を基準に縮小する。
    if image.height > resize_height:
        resize_rate= resize_height/image.height
        resize_width= int(image.width*resize_rate)
        return image.resize((resize_width,resize_height),Image.LANCZOS)
    else:
        return image

def named_from_date(image_path):
    #文字入れ後のファイル名を決める
    now = datetime.datetime.now()
    return os.path.basename(image_path).split(".")[0]+"_edited_in_"+now.strftime("%Y_%m_%d_%H_%M_%S")+".jpg"

def main(name,image_path,output_dir,resize):
    output_name=named_from_date(image_path)

    output_dir=os.path.abspath(output_dir)
    if os.path.isdir(output_dir) ==False:
        os.makedirs(output_dir)
    output_path=output_dir+"\\"+ output_name
    photo_info = photo_info_to_str(name,**get_exif_of_image(image_path))
    image_str_added=write_to_image(image_path,photo_info)
    if resize:
        image_str_added=resize_for_web(image_str_added,960)
    image_str_added.save(output_path,quality=100)


if __name__ == "__main__":
    image_path = input("画像のパスを入力")
    name =input("撮影者名を入力")
    output_dir=input("出力先フォルダを指定") or "finished"
    main(name,image_path,output_dir,True)