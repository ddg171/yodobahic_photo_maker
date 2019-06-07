#coding UTF-8
#TkinterでGUI化する

import tkinter.messagebox
import tkinter.font as font
from tkinter import filedialog as tkFileDialog
import shelve

import yodobashic_photo_maker as ypm

#基本設定
app_name = "某レビューサイトっぽく画像に文字入れするやつ"
app_size = "600x180" 

#rootウィンドウの設定
root = tkinter.Tk()
root.title(app_name)
root.geometry(app_size)
root.resizable(0,0) #ウィンドウサイズを固定

#変数
input_path_buffer =tkinter.StringVar() #文字入れ前の画像のパスを格納
output_dir_buffer =tkinter.StringVar() #出力先ディレクトリを格納
name_buffer =tkinter.StringVar() #撮影者名を格納
#resize_conf = tkinter.BooleanVar() #リサイズ設定
#resize_conf.set(True)



#設定ファイルがある場合は設定を読み出し
latest_config= shelve.open("config")
try:
    keyword_init = latest_config["keyword"]
    dir_init = latest_config["dir_"]
except KeyError:
    keyword_init = ""
    dir_init = ""
latest_config.close()

def btn1_action(event):

    #実施後に設定を保存する
    config = shelve.open("config")
    config["name"] = name
    config["output_dir"] = output_dir
    config.close()