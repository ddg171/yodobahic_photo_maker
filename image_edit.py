from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#文字列の入った画像を用意する。
#pyでは縦解像度1280に対して文字列の高さは15
#0.013*縦解像度


def image_add_str(image_path,text,font_path,margin=10):
    image =Image.open(image_path)
    font_size =int(0.013*image.height)
    font =ImageFont.truetype(font_path,font_size)

    draw = ImageDraw.Draw(image)
    
    if draw.textsize(text,font)[0]+margin>image.width:
        while draw.textsize(text+"...",font)[0]>image.width-margin:
            text= text[:-1]
        text=text+"..."
    text_wigth= draw.textsize(text,font)[0]
    draw_x=image.width-(text_wigth+margin)
    draw_y = image.height-(font_size+margin)
    draw.text((draw_x, draw_y), text, font=font, fill=(255,255,255,128))
    return image


        

if  __name__ == "__main__":
    text = "α6000,Sony E 50mm F1.8 OSS,1/4000,F1.8,ISO 100,Photo by pori"
    font_path = "C:\Windows\Fonts\meiryo.ttc"
    font_size =30

    image_add_str("sample.jpg",text,font_path,font_size).show()
    #image_add_str("sample.jpg",text,font_path,30).save("sample_added.jpg",quallity=100)
    