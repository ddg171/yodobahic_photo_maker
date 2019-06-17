#coding UTF-8
#TkinterでGUI化
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
iconfile = 'favicon.ico'
root.iconbitmap(default=iconfile)

root.grid_columnconfigure((0, 1, 2), weight=1)
root.grid_rowconfigure((0, 1, 2, 3, 4, 5,6,7,8), weight=1)

#ラベルの設定
label_font = font.Font(root, family="System",size=10, weight="normal")
#チェックボタンの設定
checkbtn_font= font.Font(root, family="System",size=12, weight="normal")
#ボタンの設定
btn_font = font.Font(root, family="System",size=7, weight="normal")
#使用するフォントの設定
font_path ="font\meiryo.ttc"

#変数
input_path_or_dir_buffer =tkinter.StringVar() #文字入れ前の画像のパスを格納
output_dir_buffer =tkinter.StringVar() #出力先ディレクトリを格納
name_buffer =tkinter.StringVar() #撮影者名を格納
resize_conf_buffer = tkinter.BooleanVar() #リサイズ設定
resize_conf_buffer.set(True)
name_only_conf_buffer= tkinter.BooleanVar()#名前のみの書き込み設定
name_only_conf_buffer.set(False)
preview_dir_buffer= tkinter.BooleanVar()#実行後に出力先フォルダを開く
preview_dir_buffer.set(True)
#TODO リサイズする解像度を選択可能にする。


#テキスト
name_entry_text="撮影者名"
input_file_or_dir_entry_text="画像またはフォルダを入力"
output_dir_entry_text="出力先フォルダ"
file_dialog_text="ファイル選択"
dir_dialog_text="フォルダ選択"
resize_check_text="画像をリサイズする"
preview_dir_text="実行後に出力先フォルダを開く"
name_only_check_text="名前のみを書き込む"

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
#名前のみ書き込む場合の設定（チェックボックス）
name_only_check=tkinter.Checkbutton(root, text= name_only_check_text, variable= name_only_conf_buffer, font=checkbtn_font)
#出力先フォルダの表示設定(チェックボックス)
preview_dir_check=tkinter.Checkbutton(root, text= preview_dir_text, variable= preview_dir_buffer, font=checkbtn_font)

def btn_execute_action(event):
    #変数の読み込み
    btn_execute.config(state="disable")
    btn_execute.config(text="実行中")
    name=name_buffer.get()
    name_only= name_only_conf_buffer.get()
    resize=resize_conf_buffer.get()
    output_dir=os.path.abspath(output_dir_buffer.get())
    preview_dir =preview_dir_buffer.get()
    input_file_or_dir=os.path.abspath(input_path_or_dir_buffer.get())

    
    confirm_text_list=[ "有" if i==True else "無"  for i in [resize,name_only,preview_dir] ]
    confirm_text="リサイズ:{0[0]},名前のみ:{0[1]},プレビュー:{0[2]} で実行します。".format(confirm_text_list)
    #変更枚数のカウンタ
    num=0
    #実行前の確認
    if tkinter.messagebox.askokcancel(title="確認",message=confirm_text):
        #出力先フォルダの決定
        try:
            #出力先フォルダが使用できないか、作業フォルダの場合
            if os.path.isfile(output_dir):
                tkinter.messagebox.showerror(title="確認",message="出力先フォルダを変更します。")
                output_dir=os.path.join( os.path.dirname(input_file_or_dir),"Finished")
            elif output_dir==os.getcwd() and os.path.isdir(input_file_or_dir):
                tkinter.messagebox.showerror(title="確認",message="出力先フォルダを変更します。")
                output_dir=os.path.join(input_file_or_dir,"Finished")
            """else:
                tkinter.messagebox.showerror(title="確認",message="出力先フォルダを変更します。")
                output_dir=os.path.join( os.path.dirname(input_file_or_dir),"Finished")"""
        except:
            tkinter.messagebox.showerror(title="異常発生",message="作業ディレクトリに出力します。")
            output_dir =os.getcwd()
        
        #入力先と出力先をエントリーに反映
        input_file_or_dir_entry.delete(0, tkinter.END)
        input_file_or_dir_entry.insert(tkinter.END,input_file_or_dir)
        output_dir_entry.delete(0, tkinter.END)
        output_dir_entry.insert(tkinter.END,output_dir)

        try:
            # ファイル単体が入力された場合
            if os.path.isfile(input_file_or_dir):
                image_path_list=[input_file_or_dir]
            # フォルダが入力された場合
            else:
                image_path_list=ypm.image_list_of(input_file_or_dir)
            image_sum=len(image_path_list)

            if tkinter.messagebox.askokcancel(title="枚数確認",message="{}枚の画像に文字入れします".format(image_sum)):
                for image_path in image_path_list:
                    num += ypm.make_photo_yodobashic(name,name_only,output_dir,resize,image_path,font_path)
                    #btn_execute_text="{0}/{1}枚完了".format(num,image_sum)
                    #btn_execute.config(text=btn_execute_text)
        except:
            tkinter.messagebox.showerror(title="異常発生",message="処理を中断します。")

        tkinter.messagebox.showinfo(title="終了",message="{}個の画像を文字入れしました。".format(num))
        
        #実施後に設定を保存する
        latest_config = shelve.open("ypm_config")
        latest_config["name"] = name
        latest_config["output_dir"] = output_dir
        latest_config.close()
    else:
        tkinter.messagebox.showinfo(title="中断",message="処理を取り止めました")
        #TODO エラーごとに表示を分ける

    if preview_dir and num>0:
        ypm.opan_dir(output_dir)
    btn_execute.config(state="active")
    btn_execute.config(text="実行")

#実行ボタン
btn_execute = tkinter.Button(text="実行", font=btn_font)
btn_execute.bind("<Button-1>", btn_execute_action)


#各ウィジェットを配置
tkinter.Label(text=name_entry_text, font=label_font).grid(row=0, column=0,sticky='w')
name_entry.grid(row=0, column=1,columnspan=4,sticky="e")

tkinter.Label(text=input_file_or_dir_entry_text, font=label_font).grid(row=2, column=0,columnspan=3,sticky='w')

input_file_or_dir_entry.grid(row=3, column=0,columnspan=4,sticky='w')

input_file_dialog.grid(row=4, column=2)
input_dir_dialog.grid(row=4, column=3)

tkinter.Label(text=output_dir_entry_text, font=label_font).grid(row=5, column=0,sticky='w')
output_dir_entry.grid(row=6, column=0,columnspan=4)
output_dir_dialog.grid(row=7, column=0,sticky='w')
resize_check.grid(row=8, column=0,columnspan=3,sticky='w')
name_only_check.grid(row=9, column=0,columnspan=3,sticky='w')
preview_dir_check.grid(row=10,column=0,columnspan=3,sticky="w")
btn_execute.grid(row=10, column=3,sticky='e')

root.mainloop()
