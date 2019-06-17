#coding UTF-8

import re
import os
import datetime
import subprocess

from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFont
#from PIL.ExifTags import TAGS

def get_exif_of_image(image):
    TAGS_lite={0x0110: "Model",0xa434: "LensModel",0x829a: "ExposureTime",0x829d: "FNumber",0x8827: "ISOSpeedRatings",0x0112: "Orientation",}
    data_requried=["Model","LensModel","ExposureTime","FNumber","ISOSpeedRatings","Orientation"]
    try:
        exif = image._getexif()
    except AttributeError:
        return {}

    exif_table = {}
    try:
        for tag_id, value in exif.items():
            tag = TAGS_lite.get(tag_id, tag_id)
            exif_table[tag] = value
    except AttributeError:
        pass

    exif_data ={}
    #縦横情報の初期値
    exif_data["Orientation"]=1
    for id in data_requried:
        try:
            if id =="Model" or id== "LensModel":
                exif_data[id]=exif_table[id]
            elif id=="ExposureTime":
                exif_data[id]=str(exif_table["ExposureTime"][0])+"/"+str(exif_table["ExposureTime"][1])
            elif id == "FNumber":
                exif_data[id]="F"+str(exif_table["FNumber"][0]/exif_table["FNumber"][1])
            elif id =="ISOSpeedRatings":
                exif_data[id]="ISO"+str(exif_table["ISOSpeedRatings"])
            #縦横判別情報も一緒に取り出しておく
            elif id == "Orientation":
                exif_data[id]=exif_table["Orientation"]
        except KeyError:
            pass
    return exif_data


def photo_info_to_str(name,name_only,**exif_data):
    #取り出したEXIF情報を一つの文字列にまとめる
    #レンズの製品名の後ろに括弧付きで型番がついている場合は削除する
    #pyでの並びは(機種)(レンズ名)(シャッター速度)(絞り)(ISO感度)Photo by(撮影者名)
    info_requried=["Model","LensModel","ExposureTime","FNumber","ISOSpeedRatings"]
    exif_str=""
    try:
        exif_data["LensModel"]=re.sub(r"\s?[(].+[)]","",exif_data["LensModel"])
    except KeyError:
        pass
    if name_only == False:
        for id in info_requried:
            try:
                exif_str += exif_data[id]+","
            except KeyError:
                pass
    if name == "":
        exif_str=exif_str[:-1]
    else:
        exif_str +="Photo by "+name
    return exif_str

def color_check(image_cropped):
    #文字の背景に合わせて文字色を決める
    threshold =100
    color_white =(240,240,240,100)
    color_black =(30,30,30,100)
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


def write_to_image(image,text,font_path):
    #文字列を画像に書き込む
    font_size =int(0.016*image.height)
    margin =font_size
    font =ImageFont.truetype(font_path,font_size)
    draw = ImageDraw.Draw(image)
    #文字数に応じて位置を調整する
    if draw.textsize(text,font)[0]+margin>image.width:
        while draw.textsize(text,font)[0]>image.width-margin:
            if font_size<13:
                break
            font_size -=1
            font =ImageFont.truetype(font_path,font_size)

    text_width= draw.textsize(text,font)[0]
    draw_x=image.width-(text_width+margin)
    draw_y = image.height-(font_size+margin)

    #背景に合わせて文字色を変更する
    color = color_check(image.crop((draw_x,draw_y,image.width,image.height)))

    draw.text((draw_x, draw_y), text, font=font, fill=color)
    return image

def resize_for_web(image,resize_length):
    if image.height>=image.width and image.width > resize_length:
        resize_rate= resize_length/image.width
        resize_height= int(image.height*resize_rate)
        resize_width= resize_length
        return image.resize((resize_width,resize_height),Image.LANCZOS)
    elif image.height > resize_length:
        resize_rate= resize_length/image.height
        resize_height =resize_length
        resize_width= int(image.width*resize_rate)
        return image.resize((resize_width,resize_height),Image.LANCZOS)
    else:
        return image

def rotate_image(image,orientation):
    #EXIF情報に基づいて画像を回転する
    if orientation ==8:
        return image.rotate(90,expand=True)
    elif orientation==7:
        return image.rotate(90,expand=True).mirror()
    elif orientation==6:
        return image.rotate(270,expand=True)
    elif orientation==5:
        return image.rotate(90,expand=True).flip()
    elif orientation==4:
        return image.mirror()
    elif orientation==3:
        return image.rotate(180,expand=True)
    elif orientation==2:
        return image.mirror()
    else:
        return image


def named_from_date(image_path):
    #文字入れ後のファイル名を決める
    now = datetime.datetime.now()
    return os.path.basename(image_path).split(".")[0]+"_edited_in_"+now.strftime("%Y_%m_%d_%H_%M_%S")+".jpg"

def image_list_of(dir_):
    #jpegファイルを検索するための正規表現
    image_re_condtion=r".jpg|.jpeg"
    image_re =re.compile(image_re_condtion,re.I)
    #フォルダ内のファイル・フォルダ一覧からjpgファイルを抽出
    """jpg_list=[]
    for item in os.listdir(dir_):
        if os.path.isfile(dir_+ "\\"+item) and (image_re.search(item)!= None):
            jpg_list.append(dir_+"\\"+item)
    return jpg_list"""
    return [dir_+"\\"+item  for item in os.listdir(dir_)  if os.path.isfile(dir_+ "\\"+item) and (image_re.search(item)!= None)]
    


def make_photo_yodobashic(name,name_only,output_dir,resize,image_path,font_path):
    try:
        image=Image.open(image_path)
    except IOError:
        pass 
        #TODO なんか良い対応を考える
    #出力ファイルの名前を決める
    output_name= named_from_date(image_path)
    #出力先を決める
    output_dir=os.path.abspath(output_dir)
    if os.path.isdir(output_dir) ==False: #フォルダが存在しない場合の対応
        os.makedirs(output_dir)
    output_path=output_dir+"\\"+ output_name
    #EXIF情報の取り出し
    exif_data= get_exif_of_image(image)
    orientation= exif_data["Orientation"]
    #exif情報から画像を回転させる
    if orientation != 1:
        image =rotate_image(image,orientation)
    #必要ならリサイズ
    if resize:
        image =resize_for_web(image,1280)
    #書き込む文字列の整形
    photo_info = photo_info_to_str(name,name_only,**exif_data)
    #書き込み
    image_str_added=write_to_image(image,photo_info,font_path)
    """if resize: #必要ならリサイズ
        image_str_added=resize_for_web(image_str_added,1280)"""
    image_str_added.save(output_path,quality=100)
    return 1




def make_photo_yodobashic_continuous(name,name_only,output_dir,resize,image_dir,font_path):
    num =0
    if os.path.isdir(image_dir)==True:
        for image_path in image_list_of(image_dir):
            num += make_photo_yodobashic(name,name_only,output_dir,resize,image_path,font_path)
    return num

def opan_dir(path):
    if os.path.isdir(path):
        subprocess.Popen(r'explorer "{}"'.format(path))


if __name__ == "__main__":
    resize=True
    name_only=True
    name =input("撮影者名を入力")
    output_dir=input("出力先フォルダを指定") or "finished"
    if input("リサイズしますか？(Y/N)\n") ==("n" or "N"):
        resize = False
    print("ループ処理開始")
    while True:
        image_path = input("画像のパスを入力\n")
        if image_path !="":
            make_photo_yodobashic(name,name_only,output_dir,resize,image_path)
            print("完了")
        else:
            print("終了")
            break
