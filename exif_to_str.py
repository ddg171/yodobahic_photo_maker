#coding UTF-8

import re

#取り出したexif情報を整形して文字列として出力する。
#maker_list =[r"sony",r"canon",r"nikon",r"pentax"]
model_list ={"ILCE-6000":"α6000"}

photo_info =['ILCE-6000', 'Sony E 50mm F1.8 OSS (SEL50F18)', '1/4000', 'F1.8', 'ISO 100']


def phoyo_info_to_str(name,*photo_info):
    photo_str=""
    #カメラの形式を製品名に変換
    for number,model_name in model_list.items():
        if photo_info[0] == number:
            photo_str = photo_str+model_name
    
    #レンズの製品名の後ろに括弧付きで型番がついている場合は削除する
    photo_str=photo_str+", "+re.sub(r"\s?[(].+[)]","",photo_info[1])

    return photo_str+", "+photo_info[2]+", "+photo_info[3]+", "+photo_info[4]+", Photo by "+name

output=phoyo_info_to_str("pori",*photo_info)



if __name__ == "__main__":
    print(output)
    print(len(output))

#α6000, Sony E 50mm F1.8 OSS, 1/4000, F1.8, ISO 100, Photo by Hoge
#65
