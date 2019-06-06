from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#文字列の入った画像を用意する。
#pyでは縦解像度1280に対して文字列の高さは15



def image_add_str(image_path,text,font_path,font_size):
    image =Image.open(image_path)
    
    font =ImageFont.truetype(font_path,font_size)

    draw = ImageDraw.Draw(image)
    text_wigth= draw.textsize(text,font)[0]
    draw_x=image.width-(text_wigth+15)
    draw_y = image.height-(font_size+15)
    draw.text((draw_x, draw_y), text, font=font, fill=(255,255,255,128))
    return image

if  __name__ == "__main__":
    text = "α6000, Sony E 50mm F1.8 OSS, 1/4000, F1.8, ISO 100, Photo by Hogehogehogehoge"
    font_path = "C:\Windows\Fonts\meiryo.ttc"

    image_add_str("sample.jpg",text,font_path,20).save("sample_added.jpg",quallity=100)
    