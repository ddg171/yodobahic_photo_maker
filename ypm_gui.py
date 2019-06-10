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
app_size = "400x280" 

#rootウィンドウの設定
root = tkinter.Tk()
root.title(app_name)
root.geometry(app_size)
root.resizable(0,0) #ウィンドウサイズを固定

root.grid_columnconfigure((0, 1, 2), weight=1)
root.grid_rowconfigure((0, 1, 2, 3, 4, 5,6,7,8), weight=1)

#ラベルの設定
label_font = font.Font(root, family="System",size=12, weight="normal")
#チェックボタンの設定
checkbtn_font= font.Font(root, family="System",size=14, weight="normal")
#ボタンの設定
btn_font = font.Font(root, family="System",size=9, weight="normal")

#変数
input_path_or_dir_buffer =tkinter.StringVar() #文字入れ前の画像のパスを格納
output_dir_buffer =tkinter.StringVar() #出力先ディレクトリを格納
name_buffer =tkinter.StringVar() #撮影者名を格納
resize_conf_buffer = tkinter.BooleanVar() #リサイズ設定
resize_conf_buffer.set(True)

#テキスト
name_entry_text="撮影者名"
input_file_or_dir_entry_text="画像またはフォルダを入力"
output_dir_entry_text="出力先フォルダ"
file_dialog_text="ファイル"
dir_dialog_text="フォルダ"
resize_check_text="リサイズする場合はチェック"

#設定ファイルがある場合は設定を読み出し
latest_config= shelve.open("ypm_config")
name_init = ""
output_dir_init = ""
try:
    name_init = latest_config["name"]
    output_dir_init = latest_config["output_dir"]
except KeyError:
    pass
latest_config.close()


#UI
# 撮影者名入力（エントリー）

name_entry = tkinter.Entry(root, textvariable=name_buffer)
name_entry.insert(tkinter.END,name_init) 


# 画像ファイル入力（エントリー、ファイルダイアログ、フォルダダイアログ）

input_file_or_dir_entry = tkinter.Entry(root, textvariable=input_path_or_dir_buffer,width=70)


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


input_dir_dialog = tkinter.Button(text=dir_dialog_text, font=btn_font)
input_dir_dialog.bind("<Button-1>",input_dir_dialog_action)


# 出力先フォルダ指定（エントリー、フォルダダイアログ）

output_dir_entry = tkinter.Entry(root, textvariable=output_dir_buffer,width=70)
output_dir_entry.insert(tkinter.END, output_dir_init)


#ダイアログ使用時の動作
def output_dir_dialog_action(event):
    output_dir_entry.delete(0, tkinter.END)
    output_dir_dialog=tkFileDialog.askdirectory()
    output_dir_entry.insert(tkinter.END, output_dir_dialog)

#GUIでのフォルダ選択ボタン
output_dir_dialog = tkinter.Button(text=dir_dialog_text, font=btn_font)
output_dir_dialog.bind("<Button-1>",output_dir_dialog_action)


#リサイズ設定（チェックボックス）
resize_check=tkinter.Checkbutton(root, text= resize_check_text, variable= resize_conf_buffer, font=checkbtn_font)


def btn_execute_action(event):
    btn_execute.config(state="disable")
    name=name_buffer.get()
    resize=resize_conf_buffer.get()
    output_dir=output_dir_buffer.get()
    input_file_or_dir=input_path_or_dir_buffer.get()
    num=0
        # ファイル単体が入力された場合
    try:
        if os.path.isfile(input_file_or_dir):
                # 出力先ディレクトリが使用できない場合
            if os.path.isdir(output_dir) != True or output_dir=="":
                tkinter.messagebox.showerror(title="出力フォルダ選択不可",message="出力先フォルダを変更しました。")
                output_dir =os.path.abspath("finished")
            image_path= input_file_or_dir
            num = ypm.make_photo_yodobashic(name,output_dir,resize,image_path)
        # フォルダが入力された場合
        else :
            image_dir = input_file_or_dir
            # 出力先ディレクトリが使用できない場合
            if os.path.isdir(output_dir) != True or output_dir=="":
                tkinter.messagebox.showerror(title="出力フォルダ選択不可",message="出力先フォルダを変更しました。")
                output_dir =input_file_or_dir +"\\"+"finished"
            image_path= input_file_or_dir
            num = ypm.make_photo_yodobashic_continuous(name,output_dir,resize,image_dir)
    except:
        tkinter.messagebox.showerror(title="異常発生",message="処理を中断します。")


    #実施後に設定を保存する
    latest_config = shelve.open("ypm_config")
    latest_config["name"] = name
    latest_config["output_dir"] = output_dir
    latest_config.close()
    if num==0:
        tkinter.messagebox.showinfo(title="確認",message="文字入れ対象の画像はありませんでした。")
    else:
        tkinter.messagebox.showinfo(title="終了",message="{}個の画像を文字入れしました。".format(num))
    btn_execute.config(state="active")


#実行ボタン
btn_execute = tkinter.Button(text="実行", font=btn_font)
btn_execute.bind("<Button-1>", btn_execute_action)


#各ウィジェットを配置

tkinter.Label(text=name_entry_text, font=label_font).grid(row=0, column=0,sticky='w')
name_entry.grid(row=0, column=1,columnspan=3)

tkinter.Label(text=input_file_or_dir_entry_text, font=label_font).grid(row=2, column=0,columnspan=3,sticky='w')

input_file_or_dir_entry.grid(row=3, column=0,columnspan=4,sticky='w')

input_file_dialog.grid(row=4, column=2)
input_dir_dialog.grid(row=4, column=3)

tkinter.Label(text=output_dir_entry_text, font=label_font).grid(row=5, column=0,sticky='w')
output_dir_entry.grid(row=6, column=0,columnspan=4)
output_dir_dialog.grid(row=7, column=0,sticky='w')
resize_check.grid(row=8, column=0,columnspan=3,sticky='w')
btn_execute.grid(row=9, column=3,sticky='E')

root.mainloop()
