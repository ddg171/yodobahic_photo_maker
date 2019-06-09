#coding UTF-8
#TkinterでGUI化する
import os

import tkinter.messagebox
import tkinter.font as font
from tkinter import filedialog as tkFileDialog
import shelve

import yodobashic_photo_maker as ypm

#基本設定
app_name = "某家電量販店っぽく画像に文字入れするやつ"
app_size = "600x280" 

#rootウィンドウの設定
root = tkinter.Tk()
root.title(app_name)
root.geometry(app_size)
root.resizable(0,0) #ウィンドウサイズを固定

#ラベルの設定
label_font = font.Font(root, family="System",size=14, weight="normal")
#チェックボタンの設定
checkbtn_font= font.Font(root, family="System",size=16, weight="normal")
#ボタンの設定
btn_font = font.Font(root, family="System",size=12, weight="normal")

#変数
input_path_or_dir_buffer =tkinter.StringVar() #文字入れ前の画像のパスを格納
output_dir_buffer =tkinter.StringVar() #出力先ディレクトリを格納
name_buffer =tkinter.StringVar() #撮影者名を格納
resize_conf = tkinter.BooleanVar() #リサイズ設定
resize_conf.set(True)

#テキスト
name_entry_text="撮影者名"
input_file_or_dir_entry_text="画像またはフォルダを入力(フォルダの場合は中の画像を全て加工)"
output_dir_entry_text="出力先フォルダ"
file_dialog_text="ファイルを選択"
dir_dialog_text="フォルダ選択"
resize_check_text="リサイズする場合はチェック"

#設定ファイルがある場合は設定を読み出し
latest_config= shelve.open("ypm_config")
try:
    name_init = latest_config["name"]
    output_dir_init = latest_config["output_dir"]
except KeyError:
    name_init = ""
    output_dir_init = ""
latest_config.close()


#UI
# 撮影者名入力（エントリー）
tkinter.Label(text=name_entry_text, font=label_font).pack()
name_entry = tkinter.Entry(root, textvariable=name_buffer,width=70)
name_entry.insert(tkinter.END,name_init) 
name_entry.pack(anchor = 'w', fill="both" )

# 画像ファイル入力（エントリー、ファイルダイアログ、フォルダダイアログ）
tkinter.Label(text=input_file_or_dir_entry_text, font=label_font).pack()
input_file_or_dir_entry = tkinter.Entry(root, textvariable=input_path_or_dir_buffer, width=70)
input_file_or_dir_entry.pack(anchor = 'w',fill="both" )

#ダイアログ使用時の動作
def input_file_dialog_action(event):
    input_file_or_dir_entry.delete(0, tkinter.END)
    input_file_dialog=tkFileDialog.askopenfilename(filetypes=(("jpeg files","*.jpg"),("all files","*.*")),initialdir=os.path.abspath(os.path.dirname(__file__)) )
    input_file_or_dir_entry.insert(tkinter.END, input_file_dialog)


def input_dir_dialog_action(event):
    input_file_or_dir_entry.delete(0, tkinter.END)
    input_dir_dialog=tkFileDialog.askdirectory()
    input_file_or_dir_entry.insert(tkinter.END, input_dir_dialog)

# GUIでのファイル選択ボタン
input_file_dialog = tkinter.Button(text=file_dialog_text, font=btn_font)
input_file_dialog.bind("<Button-1>",input_file_dialog_action)
input_file_dialog.pack(anchor = 'w',fill="both" )

input_dir_dialog = tkinter.Button(text=dir_dialog_text, font=btn_font)
input_dir_dialog.bind("<Button-1>",input_dir_dialog_action)
input_dir_dialog.pack(anchor = 'w')

# 出力先フォルダ指定（エントリー、フォルダダイアログ）
tkinter.Label(text=output_dir_entry_text, font=label_font).pack()
output_dir_entry = tkinter.Entry(root, textvariable=output_dir_buffer, width=70)
output_dir_entry.insert(tkinter.END, output_dir_init)
output_dir_entry.pack(anchor = 'w',fill="both" )

#ダイアログ使用時の動作
def output_dir_dialog_action(event):
    output_dir_entry.delete(0, tkinter.END)
    output_dir_dialog=tkFileDialog.askdirectory()
    output_dir_entry.insert(tkinter.END, output_dir_dialog)

#GUIでのフォルダ選択ボタン
output_dir_dialog = tkinter.Button(text=dir_dialog_text, font=btn_font)
output_dir_dialog.bind("<Button-1>",output_dir_dialog_action)
output_dir_dialog.pack(anchor = 'w')

#リサイズ設定（チェックボックス）
resize_check=tkinter.Checkbutton(root, text= resize_check_text, variable= resize_conf, font=checkbtn_font)
resize_check.pack(anchor = 'w' ) 

def btn_execute_action(event):
    name=name_buffer
    resize=resize_conf
    output_dir=output_dir_buffer
    input_file_or_dir=input_path_or_dir_buffer
    # 出力先ディレクトリが使用できない場合
    if os.path.isdir(output_dir) != False:
        output_dir =""

    #TODO ファイル単体が入力された場合
    if os.path.isfile(input_file_or_dir):
        image_path= input_file_or_dir
        pym.make_photo_yodobashic(name,image_path,output_dir,resize)

    #TODO フォルダが入力された場合
    elif os.path.isdir(input_path_or_dir):
        file_list_all=os.list
        pass
    



    #TODO フォルダが入力された場合
    



    #実施後に設定を保存する
    config = shelve.open("config")
    config["name"] = name
    config["output_dir"] = output_dir
    config.close()


#TODO 実行ボタン
btn_execute = tkinter.Button(text="実行", font=btn_font)
btn_execute.bind("<Button-1>", btn_execute_action)
btn_execute.pack(anchor = 'se' )

root.mainloop()
