#coding UTF-8

import re

#取り出したexif情報を整形して文字列として出力する。
#maker_list =[r"sony",r"canon",r"nikon",r"pentax"]
model_list ={"ILCE-6000":"α6000","ILCE-6300":"α6300","ILCE-6500":"α6500"}

exif_data ={'ExposureTime':'1/4000','FNumber':'F1.8','ISOSpeedRatings':'ISO 100','LensModel':'Sony E 50mm F1.8 OSS (SEL50F18)','Model':'ILCE-6000'}
#exif_data ={'ExposureTime': '1/1600','FNumber': 'F3.5','ISOSpeedRatings': 'ISO 125', 'Model': 'DSC-RX100M5'}

def phoyo_info_to_str(name,**exif_data):
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
    exif_str +="Photo by "+name
    return exif_str

if __name__ == "__main__":
    print(exif_data)
    output=phoyo_info_to_str("pori",**exif_data)
    print(output)
    #print(len(output))

#α6000,Sony E 50mm F1.8 OSS,1/4000,F1.8,ISO 100,Photo by pori
#DSC-RX100M5,1/1600,F3.5,ISO 125,Photo by pori
