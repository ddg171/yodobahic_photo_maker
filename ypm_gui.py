#coding UTF-8
#TkinterでGUI化する

import yodobashic_func as py

import tkinter.messagebox
import tkinter.font as font
from tkinter import filedialog as tkFileDialog

#基本設定
app_name = "某レビューサイトっぽく画像に文字入れするやつ"
app_size = "600x180" 

#rootウィンドウの設定
root = tkinter.Tk()
root.title(app_name)
root.geometry(app_size)
root.resizable(0,0) #ウィンドウサイズを固定