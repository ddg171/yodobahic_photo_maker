#coding UTF-8
#TkinterでGUI化する

import tkinter.messagebox
import tkinter.font as font
from tkinter import filedialog as tkFileDialog
import shelve

import yodobashic_photo_maker as ypm

#基本設定
app_name = "某家電量販店っぽく画像に文字入れするやつ"
app_size = "600x200" 

#rootウィンドウの設定
root = tkinter.Tk()
root.title(app_name)
root.geometry(app_size)
root.resizable(0,0) #ウィンドウサイズを固定

#変数
input_path_or_dir_buffer =tkinter.StringVar() #文字入れ前の画像のパスを格納
output_dir_buffer =tkinter.StringVar() #出力先ディレクトリを格納
name_buffer =tkinter.StringVar() #撮影者名を格納
#resize_conf = tkinter.BooleanVar() #リサイズ設定
#resize_conf.set(True)


#設定ファイルがある場合は設定を読み出し
latest_config= shelve.open("ypm_config")
try:
    name_init = latest_config["name"]
    output_dir_init = latest_config["output_dir"]
except KeyError:
    name_init = ""
    output_dir_init = ""
latest_config.close()

def btn_execute_action(event):

    #実施後に設定を保存する
    config = shelve.open("config")
    config["name"] = name
    config["output_dir"] = output_dir
    config.close()

#UI
#TODO 撮影者名入力（エントリー）

#TODO 画像ファイル入力（エントリー、ファイルダイアログ、フォルダダイアログ）

#TODO 出力先フォルダ指定（エントリー、フォルダダイアログ）

#TODO リサイズ設定（チェックボックス）

#TODO 実行ボタン

