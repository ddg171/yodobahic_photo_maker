#coding UTF-8

import re
import os
import datetime

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL.ExifTags import TAGS

model_list ={"ILCE-6000":"α6000","ILCE-6300":"α6300","ILCE-6400":"α6400","ILCE-6500":"α6500"}
data_requried=["Model","LensModel","ExposureTime","FNumber","ISOSpeedRatings"]
font_path = "font\meiryo.ttc"

def get_exif_of_image(file):
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


def phoyo_info_to_str(name,**exif_data):
    #取り出したEXIF情報を一つの文字列にまとめる
    #カメラの形式を製品名に変換
    try:
        for number,model_name in model_list.items():
            if exif_data["Model"] == number:
                exif_data["Model"]= model_name
    except KeyError:
        pass
    #レンズの製品名の後ろに括弧付きで型番がついている場合は削除する
    try:
        exif_data["LensModel"]=re.sub(r"\s?[(].+[)]","",exif_data["LensModel"])
    except KeyError:
        pass
    
    data_requried=["Model","LensModel","ExposureTime","FNumber","ISOSpeedRatings"]
    exif_str=""
    for id in data_requried:
        try:
            exif_str += exif_data[id]+","
        except KeyError:
            pass
    if name =="":
        exif_str=exif_str[:-1]
    else:
        exif_str +="Photo by "+name
    return exif_str


def image_add_str(image_path,text,font_path):
    threshold_color =230
    color_white =(240,240,240,120)
    color_black =(30,30,30,120)
    
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
    image_cropped = image.crop((draw_x,draw_y,image.width,image.height))
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

    if red_ave >threshold_color and green_ave>threshold_color and blue_ave>threshold_color:
        color = color_white
    else:
        color=color_black

    draw.text((draw_x, draw_y), text, font=font, fill=color)
    return image


def main(name,image_path,output_dir):
    now = datetime.datetime.now()
    output_name=os.path.basename(image_path).split(".")[0]+"_edited_in_"+now.strftime("%Y_%m_%d_%H_%M_%S")+".jpg"
    output_dir=os.path.abspath(output_dir)
    if os.path.isdir(output_dir) ==False:
        os.makedirs(output_dir)
    output_path=output_dir+"\\"+ output_name
    print(output_path)

    image_str_added=image_add_str(image_path,phoyo_info_to_str(name,**get_exif_of_image(image_path)),font_path)
    image_str_added.save(output_path,quality=100)


if __name__ == "__main__":
    image_path = input("画像のパスを入力")
    name =input("撮影者名を入力")
    output_dir=input("出力先フォルダを指定") or "finished"
    main(name,image_path,output_dir)
