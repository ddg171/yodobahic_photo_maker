import pprint
import re
import os
from PIL import Image
import yodobashic_photo_maker as ypm
#import yodobashic_photo_maker as pym



if __name__ == "__main__":
    dir_=input("入力")
    list_jpg=ypm.image_list_of(dir_)
    print(list_jpg)
    print(len(list_jpg))




    """name ="poripori"
    output_dir="finished"
    image_path = "image\\sample.JPG"
    image=Image.open(image_path)
    exif_data= pym.get_exif_of_image(image)
    orientation= exif_data["Orientation"]
    pprint.pprint(exif_data)
    image=pym.rotate_image(image,orientation)
    image.show()"""

