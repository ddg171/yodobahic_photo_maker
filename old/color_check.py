#coding UTF-8
#文字を貼り付ける範囲の色を調べ、文字色を白か黒のどちらにするのが良いか判別するプログラム

from PIL import Image
import numpy as np

image= Image.open("image\sample.jpg",)

text="α6000,Sony E 50mm F1.8 OSS,1/4000,F1.8,ISO 100,Photo by hata"
text_width=839
draw_x=1536
draw_y=1550


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

print(red_ave)
print(green_ave)
print(blue_ave)

threshold_color =220
if red_ave >threshold_color and green_ave>threshold_color and blue_ave>threshold_color:
    color = (0,0,0,128)
else:
    color=(255,255,255,128)

return color



