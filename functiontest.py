import pprint
from PIL import Image
import yodobashic_photo_maker as pym

if __name__ == "__main__":
    name ="poripori"
    output_dir="finished"
    image_path = "image\\sample.JPG"
    image=Image.open(image_path)
    exif_data= pym.get_exif_of_image(image)
    orientation= exif_data["Orientation"]
    pprint.pprint(exif_data)
    image=pym.rotate_image(image,orientation)
    image.show()

