# https://stackoverflow.com/questions/1905421/crop-a-png-image-to-its-minimum-size

import os
import glob
from PIL import Image

folder_dir = "images/folder/path/"

# Find all files in folders and subfolders
folders = [f for f in glob.glob(folder_dir + "**/*", recursive=True)]

# Change output file extinsion to "png" and append "Cropped" string to its name
# def append_id(filename):
#   p = Path(filename)
#  return "{0}_{2}{1}".format(Path.joinpath(p.parent, p.stem), ".png", "Cropped")


def autocrop_image(image, border=0):
    # Get the bounding box
    bbox = image.getbbox()

    # Crop the image to the contents of the bounding box
    image = image.crop(bbox)

    # Determine the width and height of the cropped image
    (width, height) = image.size

    # Add border
    width += border * 2
    height += border * 2

    # Create a new image object for the output image
    cropped_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    # Paste the cropped image onto the new image
    cropped_image.paste(image, (border, border))

    # Done!
    return cropped_image


# Itirate all the found files to filter only images
for img in folders:

    if img.endswith(".png"):
        # get image full path (with extinsion)
        input_path = os.path.abspath(img)
        # print(input_path)
        # modifiy the output image name and extinsion
        output_path = input_path
        # print(output_path)

        # Cropping work

        # Open the input image
        image = Image.open(input_path)

        # Do the cropping
        image = autocrop_image(image, 0)

        # Save the output image
        image.save(output_path)
